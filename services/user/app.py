# 匯入必要的模組
import os
import uuid
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import Blueprint
from utils import db

# 產生用戶服務藍圖
user_bp = Blueprint('user', __name__)

#--------------------------
# 在user服務藍圖加入路由
#--------------------------

# 获取当前脚本所在的目录路径
current_directory = os.path.dirname(os.path.realpath(__file__))
# 获取项目根目录路径
root_directory = os.path.abspath(os.path.join(current_directory, '..', '..'))
# 构建相对路径
UPLOAD_FOLDER = os.path.join(root_directory, 'static', 'user_icon')
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

# 定義函式來檢查文件擴展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/user_data', methods=['GET', 'POST'])
def user_data():
    # 從 session 中獲取用戶的 Email
    User_id = session.get('User_id')
    # 根據 Email 查詢用戶數據
    sql_command = f"SELECT * FROM user where user_id='{User_id}'"
    data = db.get_data(sql_command)
    # 提取用戶數據中的相關信息
    User_id = data[0][0]
    User_name = data[0][1]
    Google_id = data[0][3]
    Email = data[0][4]
    img = data[0][5]
    register_time = data[0][8]

    # 如果是 POST 請求，處理用戶上傳的文件
    if request.method == "POST":
        User_name=request.form['User_name']
        Email=request.form['Email']
        filename=img
        if 'file' not in request.files:
            # 如果沒有選擇文件，則不執行文件上傳操作
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            # 文件名安全化處理並加上唯一值
            filename = str(uuid.uuid4()) + '_'+secure_filename(file.filename)
            # 將文件保存到指定目錄
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # 更新用戶資料
            sql_command = f"UPDATE user SET user_name='{User_name}',email='{Email}',image='../static/user_icon/{filename}' WHERE user_id='{User_id}'"
        else:
            sql_command = f"UPDATE user SET user_name='{User_name}',email='{Email}' WHERE user_id='{User_id}'"
        db.edit_data(sql_command)
        # 重定向到用戶資料頁面
        return redirect(url_for('user.user_data'))
    else:
        # 如果是 GET 請求，將用戶數據傳遞給模板並返回相應的頁面
        return render_template('./user_data.html', User_id=User_id, User_name=User_name, Google_id=Google_id, Email=Email, img=img, register_time=register_time)
