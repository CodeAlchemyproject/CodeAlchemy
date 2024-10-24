# 匯入模組
from flask import request, render_template,redirect, session, jsonify
from flask_login import login_required
from flask import Blueprint
from datetime import datetime

from utils import db

# 產生回饋服務藍圖
feedback_bp = Blueprint('feedback_bp', __name__)

#新增回饋表單
@feedback_bp.route('/create/form')
def feedback_create_form():
    return render_template('feedback_create_form.html') 

# 新增回饋
@feedback_bp.route('/create', methods=['POST'])
def submit_feedback():
    feedback_content = request.form['feedback_content']
    user_id = session.get('User_id')  # 避免直接索引，使用 get 方法會安全些

    if feedback_content and user_id:
        try:
            # 取得資料庫連線 
            connection = db.connection() 
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 將回饋資料存入資料庫
            cursor = connection.cursor()
            cursor.execute("INSERT INTO feedback (user_id, content, created_at) VALUES (%s, %s, %s)",
                            (user_id, feedback_content, created_at))
            
            # 提交變更並關閉連線
            connection.commit()
            connection.close()

            # 返回成功訊息作為 JSON
            return jsonify({"status": "success", "message": "送出成功!"})
        
        except Exception as e:
            # 捕捉例外情況，並返回錯誤訊息
            print(f"Error: {e}")
            return jsonify({"status": "error", "message": "提交失敗，請稍後再試!"})
    
    else:
        # 如果 feedback_content 為空或無法獲取 user_id
        return jsonify({"status": "error", "message": "內容不能為空!"})
        
#回饋紀錄
@feedback_bp.route('/feedback_history')
def feedback_history(): 
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     

    #取得傳入參數, 執行sql命令並取回資料 
    user_id = session.get('User_id')
    cursor.execute('SELECT * FROM feedback  WHERE user_id=%s ORDER BY created_at DESC', (user_id,))
    feedback_history = cursor.fetchall()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    return render_template('feedback_history.html', feedback_history=feedback_history) 

#管理者回饋紀錄
@feedback_bp.route('/admin_dashboard')
def admin_dashboard():
    # 取得當前頁碼，默認為 1
    page = request.args.get('page', 1, type=int)
    per_page = 5

    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor() 

    # 查詢所有回饋的總數量
    cursor.execute('SELECT COUNT(*) FROM feedback')
    total_feedback = cursor.fetchone()[0]

    # 計算總頁數
    total_pages = (total_feedback + per_page - 1) // per_page

    # 計算分頁所需的偏移量
    offset = (page - 1) * per_page

    # 查詢特定頁面的回饋資料，按提交時間降序排列，並進行表連接
    query = '''
    SELECT feedback.feedback_id, user.user_name, feedback.content, feedback.created_at, feedback.reply 
    FROM feedback 
    JOIN user ON feedback.user_id = user.user_id 
    ORDER BY feedback.created_at DESC 
    LIMIT %s OFFSET %s
    '''
    cursor.execute(query, (per_page, offset))
    feedback = cursor.fetchall()
   
    #關閉連線   
    connection.close()  

    print(f'Page: {page}, Total Pages: {total_pages},{total_feedback}')


    return render_template('admin_dashboard.html', feedback=feedback, page=page, total_pages=total_pages)

#回覆回饋表單
@feedback_bp.route('/reply_feedback/form', methods=['GET'])
def reply_feedback_form():
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()
    
    feedback_id = request.args.get('feedback_id')
    query = '''
    SELECT feedback.feedback_id, user.user_name, feedback.content 
    FROM feedback 
    JOIN user ON feedback.user_id = user.user_id 
    WHERE feedback.feedback_id=%s
    '''
    cursor.execute(query, (feedback_id,))
    feedback = cursor.fetchone()
    
    #渲染網頁
    return render_template('reply_feedback_form.html', feedback=feedback) 

#回覆回饋
@feedback_bp.route('/reply_feedback', methods=['POST'])
def reply_feedback():
    #取得資料庫連線 
    connection = db.connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor() 

    feedback_id = request.form['feedback_id']
    reply_content = request.form['reply_content']
    if feedback_id and reply_content:
        # 更新資料庫中的回覆欄位
        cursor.execute('UPDATE feedback SET reply=%s WHERE feedback_id=%s', (reply_content, feedback_id))
        connection.commit()

        #關閉連線   
        connection.close() 

        # 使用 JavaScript 彈跳視窗顯示成功消息
        success_message = "送出成功!"
        return f'''
            <script>
                alert("{success_message}");
                window.location.replace("/feedback/admin_dashboard");
            </script>
        '''
    else:
        # 使用 JavaScript 彈跳視窗顯示失敗消息
        error_message = "送出失敗!"
        return f'''
            <script>
                alert("{error_message}");
                window.location.replace("/feedback/admin_dashboard");
            </script>
        '''