# 匯入模組
from flask import request, render_template,redirect,session
from flask_login import login_required
from flask import Blueprint
from datetime import datetime

from utils import db

# 產生反饋服務藍圖
feedback_bp = Blueprint('feedback_bp', __name__)

#新增反饋表單
@feedback_bp.route('/create/form')
#@login_required
def feedback_create_form():
    return render_template('feedback_create_form.html') 

#新增反饋
@feedback_bp.route('/create', methods=['POST'])
#@login_required
def submit_feedback():
    feedback_content = request.form['feedback_content']
    #user_id = request.form.get('user_id')
    user_id = session['User_id']
    if feedback_content:
        #取得資料庫連線 
        connection = db.connection() 
        
        # 取得目前時間
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將反饋資料存入資料庫
        cursor = connection.cursor()
        cursor.execute("INSERT INTO feedback (user_id, type, content, created_at) VALUES (%s, %s, %s, %s)",
                        (user_id, 'user', feedback_content, created_at))
        
        #關閉資料庫連線 
        connection.close()

        # 渲染成功畫面
        return render_template('create_success.html')
    else:
        # 渲染失敗畫面
        return render_template('create_fail.html')
    
#反饋紀錄
@feedback_bp.route('/feedback_history')
#@login_required
def feedback_history(): 
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     

    #取得傳入參數, 執行sql命令並取回資料  
    user_id = request.values.get('user_id').strip().upper()
    cursor.execute('SELECT * FROM feedback WHERE user_id=%s', (user_id,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    return render_template('feedback_history.html', data=data) 