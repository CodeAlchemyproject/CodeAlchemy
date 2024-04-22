# 匯入模組
from flask import request, render_template,redirect
from flask_login import login_required
from flask import Blueprint
from datetime import datetime
import getpass

from utils import db

# 產生反饋服務藍圖
feedback_bp = Blueprint('feedback_bp', __name__)

getpass.getuser()

@feedback_bp.route('/feedback/form')
def feedback_create_form():
    return render_template('feedback.html') 
#送出反饋
@feedback_bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_content = request.form['feedback_content']
    user_id = request.form.get('user_id')
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
        return render_template('feedback_success.html')
    else:
        # 渲染失敗畫面
        return render_template('feedback_fail.html')