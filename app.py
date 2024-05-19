# 引入模組
import os
from random import randint
from flask import Flask, render_template, session, request,jsonify,redirect
import math
import uuid
import re
from crawler.get_problem import ZJ_get_problem
from crawler.submit import ZeroJudge_Submit
#-----------------------

# 匯入各個服務藍圖
from services.auth.app import auth_bp
from services.problem.app import problem_bp
from services.contest.app import contest_bp
from services.feedback.app import feedback_bp
from services.user.app import user_bp
from services.manager.app import manager_bp
from utils import db
from utils.common import paginate,evaluate
from utils import dolos

# 產生主程式, 加入主畫面
app = Flask(__name__)
# google登入安全鑰匙(勿動)
app.secret_key = 'c5533f80-cedf-4e3a-94d3-b0d5093dbef4'


#主畫面
@app.route('/', methods=['GET'])
def index():
    # 取得使用者的篩選條件
    state = request.args.get('state','*',type=str)
    onlinejudge = request.args.get('onlinejudge','*',type=str)
    difficulty = request.args.get('difficulty','*',type=str)
    search = request.args.get('search','',type=str)
    condition = ' where ' #where前後的空格勿動
    sql_problem_command=f'SELECT * FROM problem'
    if search != '':
        condition += f'title like "%{search}%" and '
    if onlinejudge != '*':
        condition += f'substring_index(problem_id,"-",1)="{onlinejudge}" and '
    if difficulty != '*':
        condition += f'difficulty = "{difficulty}" and '
    if condition == ' where ':
        condition = ''
    else:
        condition = condition[:condition.rfind(' and ')]
        print(condition)
    sql_problem_command= sql_problem_command + condition
    data=db.get_data(sql_problem_command)
    # 預設第一頁
    page = request.args.get('page', 1, type=int)
    # 每頁顯示15列
    per_page = 15
    start_page = max(1, page - 1)
    end_page = min(page+3,math.ceil(paginate(data,page, per_page)[1]/per_page)+1)
    paginated_data = paginate(data,page, per_page)[0]
    #渲染網頁
    return render_template('problem_list.html',data=paginated_data,page=page,start_page=start_page,end_page=end_page,state=state,onlinejudge=onlinejudge,difficulty=difficulty,search=search)

#題目
@app.route('/problem',methods=['GET','POST'])
def problem():
    if request.method=="POST":
        # 從傳入封包取得資料
        data = request.form
        type = data.get('type')
        problem_id = data.get('problem_id')
        language = data.get('language')
        code = data.get('code')
        # 重新取得題目
        sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_problem_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        r = randint(1, len(example_inputs))
        if type == 'test':
            status = None
            run_time = None
            memory = None
            error_reason = None
            problem = {
                "id": problem_id,
                "example_input": re.sub(r'<[^>]*>', '', example_inputs[r - 1]),
                "example_output": re.sub(r'<[^>]*>', '', example_outputs[r - 1])
            }
            user_code = code
            result, message, run_time, memory = evaluate(user_code, problem)
            if result:
                # 只有在通過測試時才使用 run_time 和 memory 變量
                run_time = round(run_time * 1000, 4)
                memory =round(memory, 4)
            
            else:
                if message=="":
                    message="不明錯誤"

            return jsonify({'result':result,
                            'message':message,
                            'run_time':run_time,
                            "memory":memory})
        elif type == 'upload':
            # 定義語言對應的文件擴展名字典
            file_extensions = {
                'python': '.py',
                'text/x-java': '.java',
                'text/x-csrc': '.c',
                'text/x-c++src': '.cpp'
            }
            # 生成 6 位數的亂碼
            random_code = str(uuid.uuid4())[:6]
            # 生成隨機字串，第一個字母為英文字母
            # 如果第一個字元不是英文字母，則重新生成，直到第一個字元為英文字母
            while not random_code[0].isalpha():
                random_code = str(uuid.uuid4())[:6]
            # 構建文件路徑
            file_name = f'{random_code}_{problem_id}{file_extensions[language]}'
            file_path = os.path.join('./source', file_name)

            # 確保目錄存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # 寫入內容到文件中
            with open(file_path, 'w') as file:
                file.write(code)
            if "ZJ" in file_name:
                # 調用 ZeroJudge_Submit 函數進行題目提交
                score = ZeroJudge_Submit(file_name,session['User_id'])
                # 根據 score 的前兩個字來決定顯示不同的內容
                if score.startswith("AC"):
                    # 使用正規表達式從 score 中提取 run_time 和 memory
                    match = re.search(r'\((\d+ms),\s([\d.]+MB)\)', score)
                    if match:
                        run_time = match.group(1)
                        memory = match.group(2) 
                else:
                    if score.startswith("NA"):
                        message = "未通過所有測資點"
                    elif score.startswith("WA"):
                        message = '答案錯誤'
                    elif score.startswith("TLE"):
                        message = '執行超過時間限制'
                    elif score.startswith("MLE"):
                        message = "程序執行超過記憶體限制"
                    elif score.startswith("OLE"):
                        message = "程序輸出檔超過限制"
                    elif score.startswith("RE"):
                        message = "執行時錯誤"
                    elif score.startswith("RF"):
                        message = "使用了被禁止使用的函式"
                    elif score.startswith("CE"):
                        message = "編譯錯誤"
                    elif score.startswith("SE"):
                        message = "系統錯誤"
                    else:
                        message = "未知錯誤"
                return render_template('./problem.html', status=status, data=problem_data, example_inputs=example_inputs,
                                    example_outputs=example_outputs, run_time=run_time, memory=memory,
                                    error_reason=error_reason,like=like)
    else:
        problem_id = request.args.get('problem_id',type=str)
        sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_problem_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        like = db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}'")[0][0]
        return render_template('./problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,like=like)
@app.route('/add_problem', methods=['POST'])
def add_problem():
    if request.method == 'POST':
        data=request.form
        problem_id=data.get('problem_id')
        OJ=data.get('onlineJudge')
        if OJ=="ZeroJudge":
            ZJ_get_problem(problem_id)
    return 0

@app.route('/dolos', methods=['GET'])
def problem_dolos():
    url=dolos.submit_to_dolos('student_P.zip','dolos\\student_P.zip')
    return (redirect(url))
# 收藏
@app.route('/add_to_collection', methods=['POST'])
def add_to_collection():
    data = request.get_json()
    problem_id = data.get('problem_id')
    try:
        user_id = session['User_id']
        if db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}' and user_id='{user_id}'")[0][0]==0:
            sql_command=f"INSERT INTO collection(user_id,problem_id) VALUES ('{user_id}','{problem_id}')"
            print("GAWA")
        else:
            sql_command=f"DELETE FROM collection WHERE problem_id = '{problem_id}' and user_id='{user_id}'"
        db.edit_data(sql_command)
        return jsonify({'message': 'Item added to collection'}), 201
    except KeyError:
        return jsonify({'error': 'Missing item_id or user_id'}), 400

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(auth_bp, url_prefix='/auth')  
app.register_blueprint(problem_bp, url_prefix='/problem') 
app.register_blueprint(contest_bp, url_prefix='/contest') 
app.register_blueprint(feedback_bp, url_prefix='/feedback') 
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(manager_bp, url_prefix='/manager') 
#-------------------------
# 啟動主程式
#------------------------
# 啟動 Flask 應用程式
if __name__ == '__main__':
    # 啟動 Flask 應用程式
    app.run(host='0.0.0.0', port=80, debug=True,use_reloader=True)