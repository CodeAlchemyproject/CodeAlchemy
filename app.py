from datetime import datetime
import os
from flask import Flask, render_template, session, request,jsonify,redirect
import math
import uuid
import re
from crawler.submit import CodeAlchemy_submit, ZeroJudge_submit,TIOJ_submit
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

# 產生主程式,加入主畫面
app = Flask(__name__)
# google登入安全鑰匙(勿動)
app.secret_key = 'c5533f80-cedf-4e3a-94d3-b0d5093dbef4'

#主畫面
@app.route('/', methods=['GET'])
def index():
    # 取得使用者的篩選條件
    state = request.args.get('state', '*', type=str)
    onlinejudge = request.args.get('onlinejudge', '*', type=str)
    difficulty = request.args.get('difficulty', '*', type=str)
    tag = request.args.get('tag', '', type=str)
    search = request.args.get('search', '', type=str)

    try:
        # 檢查使用者有沒有登入
        user_id=session['User_id']
        sql_problem_command = """SELECT p.*, acceptance_data.acceptance_rate, state.result
FROM `113-CodeAlchemy`.problem AS p"""
        sql_command=f""" LEFT JOIN (
    SELECT problem_id, user_id, CASE 
            WHEN MAX(CASE WHEN result = 'Accepted' THEN 1 ELSE 0 END) = 1 
            THEN 'Accepted'
            ELSE MAX(result) -- 如果沒有 'Accepted'，返回其他最高的 result
        END AS result
    FROM `113-CodeAlchemy`.`answer record` WHERE user_id = '{user_id}'
GROUP BY problem_id, user_id"""
        sql_problem_command+=sql_command
        sql_problem_command+=""")AS state ON p.problem_id = state.problem_id"""
    except:
        sql_problem_command = """SELECT p.*, acceptance_data.acceptance_rate
FROM `113-CodeAlchemy`.problem AS p"""

    sql_problem_command += """
        LEFT JOIN (
    SELECT ar.problem_id,
        CONCAT(ROUND(SUM(CASE WHEN ar.result = 'Accepted' THEN 1 ELSE 0 END) / COUNT(ar.result) * 100, 2), '%') AS acceptance_rate
    FROM `113-CodeAlchemy`.`answer record` AS ar
    GROUP BY ar.problem_id
) AS acceptance_data ON p.problem_id = acceptance_data.problem_id"""

    condition = ' WHERE '  # where前後的空格勿動
    if tag != '':
        condition += f'p.tag LIKE "%{tag}%" AND '
    if search != '':
        condition += f'p.title LIKE "%{search}%" AND '
    if onlinejudge != '*':
        condition += f'SUBSTRING_INDEX(p.problem_id, "-", 1) = "{onlinejudge}" AND '
    if difficulty != '*':
        condition += f'p.difficulty = "{difficulty}" AND '
    try:
        user_id=session['User_id']
        if state == 'accept':
            condition += f'state.result = "Accepted" AND '
        elif state == 'error':
            condition += f'state.result IS NOT NULL AND state.result != "Accepted" AND '
        elif state == 'none':
            condition += f'state.result IS NULL AND '
    except:
        pass

    if condition == ' WHERE ':
        condition = ''
    else:
        condition = condition[:condition.rfind(' AND ')]
    sql_problem_command = sql_problem_command + condition
    data=db.get_data(sql_problem_command)
    # 預設第一頁
    page = request.args.get('page', 1, type=int)
    # 每頁顯示15列
    per_page = 15
    start_page = max(1, page - 1)
    end_page = min(page+3,math.ceil(paginate(data,page, per_page)[1]/per_page)+1)
    paginated_data = paginate(data,page, per_page)[0]
    #渲染網頁
    return render_template('problem_list.html',data=paginated_data,page=page,start_page=start_page,end_page=end_page,state=state,onlinejudge=onlinejudge,difficulty=difficulty,tag=tag,search=search)

# 確認使用者有登入
@app.route('/get_user_id', methods=['GET'])
def get_user_id():
    if 'User_id' in session:
        return jsonify({'user_id': session['User_id']})
    else:
        return jsonify({'error': 'User not logged in'}), 401
    
# 題目
@app.route('/problem', methods=['GET', 'POST'])
def problem():
    if request.method == "POST":
        # 從傳入封包取得資料
        data = request.form
        type=data.get('type')
        problem_id = data.get('problem_id')
        language = data.get('language')
        code = data.get('code')
        source = data.get('source')
        contest_id = data.get('contest_id')
        
        try:
            title = data.get('title')
        except:
            title = None
                
        print(f"Source: {source}, Contest ID: {contest_id}")  # 確認 source 和 contest_id

        # 定義語言對應的文件擴展名字典
        file_extensions = {
            'python': '.py',
            'text/x-java': '.java',
            'text/x-csrc': '.c',
            'text/x-c++src': '.cpp'
        }

        # 生成 6 位數的亂碼
        random_code = str(uuid.uuid4())[:6]
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
            score = ZeroJudge_submit(file_name, str(session['User_id']))
        elif "TIOJ" in file_name:
            score = TIOJ_submit(file_name, str(session['User_id']))
        elif "CAOJ" in file_name:
            score = CodeAlchemy_submit(file_name, str(session['User_id']),problem_id)

        result = False
        message = "測試失敗"
        run_time = 0
        memory = 0
        ensue = "Rejected"
        mime_to_language = {
            "text/x-c++src": "C++",
            "python": "Python",
            "text/x-csrc": "C",
            "text/x-java": "Java",
            # 可以根據需要繼續添加其他對應項
        }
        language = mime_to_language.get(language, "Unknown")
        if score and score[2] == 'Accepted':
            result = True
            message = "測試成功"
            run_time = score[3].replace('ms','')
            memory = score[4].replace('MB','')
            ensue = score[2]
        # 確認提交來源並插入到正確的資料表
        print(f'''
                INSERT INTO `answer record` (user_id, problem_id, result, language, run_time, memory, update_time)
                VALUES ('{session['User_id']}', '{problem_id}', '{ensue}', '{language}', '{run_time}', '{memory}', '{score[-1]}')
            ''')
        if source == 'contest':
            print(f"決策時的 Source 值: {source}")  # 確認 source 的值
            # 插入記錄到 contest_submission 資料表
            db.edit_data(f'''
                INSERT INTO `contest submission` (contest_id, user_id, problem_id, language, run_time, memory, is_finish, finish_time)
                VALUES ('{contest_id}', '{session['User_id']}', '{problem_id}', '{language}', '{run_time}', '{memory}', '{ensue}', '{score[-1]}')
            ''')
            print("成功插入到 contest_submission 資料表")  # 用於確認的訊息
        else:
            print(f"決策時的 Source 值: {source}")  # 確認 source 的值
            # 插入記錄到 answer record 資料表
            db.edit_data(f'''
                INSERT INTO `answer record` (user_id, problem_id, result, language, run_time, memory, update_time)
                VALUES ('{session['User_id']}', '{problem_id}', '{ensue}', '{language}', '{run_time}', '{memory}', '{score[-1]}')
            ''')
            
            print("成功插入到 answer record 資料表")  # 用於確認的訊息
        
        import shutil
        if result=='Accepted':
            ans_rec=db.get_data('''SELECT * FROM `113-CodeAlchemy`.`answer record` 
            order by record_id desc limit 1;''')

        # 複製檔案並保留所有的元數據（如權限、時間戳等）
        shutil.copy2(f'./sourse/{file_name}',f'./sourse/accept/{ans_rec[0]+'_'+problem_id}')
        return jsonify({
            'result': result,
            'message': message,
            'run_time': run_time,
            'memory': memory
        })
    else:
        # GET 請求處理邏輯
        
        problem_id = request.args.get('problem_id', type=str)
        source = request.args.get('source')
        contest_id = request.args.get('contest_id')

        sql_problem_command = f"SELECT * FROM problem WHERE problem_id='{problem_id}'"
        problem_data = db.get_data(sql_problem_command)

        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        video_id = problem_data[0][9]
        like = db.get_data(f"SELECT IFNULL(COUNT(*), 0) FROM collection WHERE problem_id='{problem_id}'")[0][0]

        return render_template('./problem.html', data=problem_data, example_inputs=example_inputs, example_outputs=example_outputs, like=like, video_id=video_id, source=source)



@app.route('/answer_record',methods=['GET'])
def answer_record():
    problem_id = request.args.get('problem_id',type=str)
    sql_problem_command=f"""SELECT record_id,u.user_id,image,user_name,result,language,run_time,memory,ar.update_time FROM `113-CodeAlchemy`.`answer record` as ar
                        left join `user` as u
                        on ar.user_id=u.user_id
                        where problem_id='{problem_id}'
                        order by update_time desc"""
    data=db.get_data(sql_problem_command)
    return render_template('./answer_record.html',data=data)
  
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
    
@app.route('/dolos', methods=['GET'])
def problem_dolos():
    problem_id=request.args.get('problem_id',type=str)
    code=request.args.get('language',type=str)
    zip=dolos.create_zip(problem_id,code)
    url=dolos.submit_to_dolos(zip[0],zip[1])
    return (redirect(url))

@app.route("/rank")
def rank():
    data=db.get_data(f'''
    SELECT 
    u.user_id, 
    u.user_name, 
    u.image, 
    SUM(CASE WHEN ar.result = 'Accepted' THEN 1 ELSE 0 END) AS 正確答題數,
    CONCAT(ROUND(SUM(CASE WHEN ar.result = 'Accepted' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2), '%') AS 答題正確率,
    round(avg(ar.run_time),2) as 平均執行時間,
    round(avg(ar.memory),2) as 平均使用記憶體
    FROM 
    `113-CodeAlchemy`.`answer record` AS ar
    LEFT JOIN 
    `user` AS u ON u.user_id = ar.user_id
    GROUP BY 
    u.user_id, u.user_name
    order by 正確答題數 desc;
                     ''')
    return render_template('./rank.html',data=data)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')
@app.errorhandler(Exception)
def page_not_found(error):
    return render_template('page_not_found.html')
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