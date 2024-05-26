# 引入模組
from datetime import datetime
import os
from flask import Flask, render_template, session, request,jsonify,redirect
import math
import uuid
import re
from crawler.submit import ZeroJudge_submit,TIOJ_submit
#-----------------------

# 匯入各個服務藍圖
from services.auth.app import auth_bp
from services.problem.app import problem_bp
from services.contest.app import contest_bp
from services.feedback.app import feedback_bp
from services.user.app import user_bp
from services.manager.app import manager_bp
from utils import db
from utils.common import ZJ_translated_return_abbreviation, paginate
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
        #從傳入封包取得資料
        data = request.form
        type = data.get('type')
        problem_id = data.get('problem_id')
        language = data.get('language')
        code = data.get('code')
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
            # 調用 ZeroJudge_submit 函數進行題目提交
            score = ZeroJudge_submit(file_name,session['User_id'])
            if score and score[2]=='Accepted':
                print()


        elif "TIOJ" in file_name:
            score=TIOJ_submit(file_name,str(session['User_id']))
            if score and score[2]=='Accepted':
                result=True
                message="測試成功"
                run_time=score[1]
                memory=score[2]
                
            else :
                result=False
                message="測試失敗"
                run_time=score[1]
                memory=score[2]
            ensue=score[3]

        if type == 'upload':
            # 執行 SQL 插入語句
            db.edit_data(f'''
                INSERT INTO `answer record` (user_id, problem_id, result, language, update_time)
                VALUES ({session['User_id']},{problem_id}, {ensue}, {language}, {datetime.now()})
            ''')


        return jsonify({'result':result,
            'message':message,
            'run_time':run_time,
            "memory":memory})
    else:
        problem_id = request.args.get('problem_id',type=str)
        sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_problem_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        like = db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}'")[0][0]
        return render_template('./problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,like=like)
            
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