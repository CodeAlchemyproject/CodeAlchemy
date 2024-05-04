# 引入模組
import os
import re
from flask import Flask, render_template, session, request
import csv
import math
import time
from queue import Queue
import pandas as pd
from crawler.submit import ZeroJudge_Submit
#-----------------------
from webdriver_manager.chrome import ChromeDriverManager

# 匯入各個服務藍圖
from services.problem.app import problem_bp
from services.auth.app import auth_bp
from services.contest.app import contest_bp
from services.feedback.app import feedback_bp
from utils import db, common

# 產生主程式, 加入主畫面
app = Flask(__name__)

# google登入安全鑰匙(勿動)
app.secret_key = 'c5533f80-cedf-4e3a-94d3-b0d5093dbef4'

#分頁功能
def paginate(data,page, per_page):
    offset = (page - 1) * per_page
    return data[offset: offset + per_page],len(data)

#主畫面
@app.route('/', methods=['GET'])
def index():
    # 取得使用者的篩選條件
    state = request.args.get('state','*',type=str)
    onlinejudge = request.args.get('onlinejudge','*',type=str)
    difficulty = request.args.get('difficulty','*',type=str)
    search = request.args.get('search','*',type=str)
    sql_problem_command='SELECT * FROM problem'
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
@app.route('/problem',methods=['GET'])
def problem():
    problem_id = request.args.get('problem_id',type=str)
    sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
    data=db.get_data(sql_problem_command)
    example_inputs = data[0][5].split('|||')
    example_outputs = data[0][6].split('|||')
    return render_template('./problem.html',data=data,example_inputs=example_inputs,example_outputs=example_outputs)

#題目提交
@app.route('/problem_submit', methods=['POST'])
def problem_submit():
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
    
    # 構建文件路徑
    file_path = os.path.join('./source', f'{problem_id}{file_extensions[language]}')

    #確保目錄存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    #寫入內容到文件中
    with open(file_path, 'w') as file:
        file.write(code)
        print(f"程式碼已成功寫入至 {file_path}")

    #ZeroJudge_Submit()
    
    # 開啟 CSV 文件
    with open('result.csv', 'r' ,encoding='utf-8') as csvfile:
        # 讀取所有行
        lines = csvfile.readlines()
        line = lines[-1]
        # 印出結果
        score = line.split(',')[-3]
        if "MB" in score: 
            index = score.find("MB")
            if index != -1:
                memory = score[:index + 2].strip()
            index = line.split(',')[-4].find("(")
            if index != -1:
                run_time = line.split(',')[-4][index + 1:].strip()  # 不包括 "(" 本身 
            score=line.split(',')[-4][:3][1:].strip()    
        else:
            score=score[:2]
    sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
    data=db.get_data(sql_problem_command)
    print(data)
    example_inputs = data[0][5].split('|||')
    print(example_inputs)
    example_outputs = data[0][6].split('|||')
    print(example_outputs)
    #根據 score 的前兩個字來決定顯示不同的內容
    print(1)
    if score.startswith("AC"):
        status = "通過"
        return render_template('./problem.html',status=status,data=data,example_inputs=example_inputs,example_outputs=example_outputs, run_time=run_time, memory=memory)
    elif score.startswith("NA"):
        error_reason = "未通過所有測資點"
    elif score.startswith("WA"):
        error_reason = '答案錯誤'  
    elif score.startswith("TLE"):
        error_reason='執行超過時間限制'
    elif score.startswith("MLE"):
        error_reason = "程序執行超過記憶體限制"
    elif score.startswith("OLE"):
        error_reason = "程序輸出檔超過限制"
    elif score.startswith("RE"):
        error_reason = "執行時錯誤"
    elif score.startswith("RF"):
        error_reason = "使用了被禁止使用的函式"
    elif score.startswith("CE"):
        error_reason = "編譯錯誤"
    elif score.startswith("SE"):
        error_reason = "系統錯誤"
    else:
        error_reason = "未知錯誤"
    print('GAWA')
    return render_template('./problem.html', status = '未通過', error_reason=error_reason)
        

@app.route('/user_data',methods=['GET'])
def user_data():
    Email = session.get('Email')
    sql_command=f"SELECT * FROM user where email='{Email}'"
    data=db.get_data(sql_command)
    User_id=data[0][0]
    User_name=data[0][1]
    Email=data[0][4]
    img=data[0][5]
    register_time=data[0][8]
    return render_template('./user_data.html',User_id=User_id,User_name=User_name,Email=Email,img=img,register_time=register_time)
# 在 Flask 應用程式啟動時啟動執行序
# def start_crawler_thread():
    # crawler_thread = Thread(target=os.system, args=("python ./crawler/ZJ_submit.py",))
    # crawler_thread.start() 

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(auth_bp, url_prefix='/auth')  
app.register_blueprint(problem_bp, url_prefix='/problem') 
app.register_blueprint(contest_bp, url_prefix='/contest') 
app.register_blueprint(feedback_bp, url_prefix='/feedback') 

#-------------------------
# 啟動主程式
#------------------------
# 啟動 Flask 應用程式
if __name__ == '__main__':
    # 在 Flask 應用程式啟動時，同時啟動爬蟲程式的執行緒
    # 啟動 Flask 應用程式
    app.run(host='0.0.0.0', port=80, debug=True)