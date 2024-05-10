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
def feedback_create_form():
    return render_template('feedback_create_form.html') 

#新增反饋
@feedback_bp.route('/create', methods=['POST'])
def submit_feedback():
    feedback_content = request.form['feedback_content']
    user_name = session['User_name']
    if feedback_content:
        #取得資料庫連線 
        connection = db.connection() 
        
        # 取得目前時間
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 將反饋資料存入資料庫
        cursor = connection.cursor()
        cursor.execute("INSERT INTO feedback (user_name, type, content, created_at) VALUES (%s, %s, %s, %s)",
                        (user_name, 'user', feedback_content, created_at))
        
        #關閉資料庫連線 
        connection.commit()
        connection.close()

        # 渲染成功畫面
        return render_template('create_success.html')
    else:
        # 渲染失敗畫面
        return render_template('create_fail.html')
    
#反饋紀錄
@feedback_bp.route('/feedback_history')
def feedback_history(): 
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     

    #取得傳入參數, 執行sql命令並取回資料  
    user_name = session.get('User_name')
    cursor.execute('SELECT * FROM feedback WHERE user_name=%s', (user_name,))
    feedback_history = cursor.fetchall()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    return render_template('feedback_history.html', feedback_history=feedback_history) 

#管理者反饋紀錄
@feedback_bp.route('/admin_dashboard')
def admin_dashboard():
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()    
    # 查詢所有反饋
    cursor.execute('SELECT * FROM feedback')
    feedback = cursor.fetchall()

    #關閉連線   
    connection.close()  

    return render_template('admin_dashboard.html', feedback=feedback)

#回覆反饋
@feedback_bp.route('/reply_feedback', methods=['GET', 'POST'])
def reply_feedback():
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor() 

    if request.method == 'GET':
        feedback_id = request.args.get('feedback_id')
        if feedback_id:
            # 根據 feedback_id 查詢反饋
            cursor.execute('SELECT * FROM feedback WHERE feedback_id=%s', (feedback_id,))
            data = cursor.fetchone()
            return render_template('reply_feedback.html', data=data)
        else:
            return 'Feedback ID is required.'
    elif request.method == 'POST':
        feedback_id = request.form['feedback_id']
        reply_content = request.form['reply_content']
        if feedback_id and reply_content:
            # 更新資料庫中的回覆欄位
            cursor.execute('UPDATE feedback SET reply=%s WHERE feedback_id=%s', (reply_content, feedback_id))
            connection.commit()

            #關閉連線   
            connection.close() 

            return render_template('admin_dashboard.html')
        else:
            return 'Please provide feedback ID and reply.'