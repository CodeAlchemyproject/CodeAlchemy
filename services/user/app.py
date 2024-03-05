# 匯入模組
from flask import Blueprint, render_template, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user 
from flask import Blueprint

from utils import db

# 產生使用者服務藍圖
user_bp = Blueprint('user_bp', __name__)

#---------------------------
# (登入管理)使用者的類別
#---------------------------
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
#---------------------------
# (登入管理)產生一個管理者
#---------------------------
login_manager = LoginManager()

#------------------------------
# (登入管理)取出登入者物件
#------------------------------
@login_manager.user_loader  
def user_loader(id): 
    return User(id) 
    
#---------------------------
# (登入管理)未授權頁面
#---------------------------
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')

#---------------------------
# 使用者登入表單
#---------------------------
@user_bp.route('/login/form')
def login_form():
    return render_template('login.php')

#--------------------------
# 使用者登入
#--------------------------
@user_bp.route('/login', methods=['POST'])
def user_login():
    # 取出帳號/密碼
    empno = request.form.get('empno')
    ext = request.form.get('ext')
    
    # 建立資料庫連線
    conn = db.get_connection()
    
    # 查詢使用者
    cursor = conn.cursor()    
    cursor.execute("SELECT empno, empname FROM employee WHERE empno = %s AND ext = %s", (empno, ext))
    employee = cursor.fetchone()
    
    # 判斷使用者是否存在
    if employee:
        empno, empname = employee 
        user = User(empno)   #(登入管理)產生一個user物件  
        login_user(user)     #(登入管理)在session中保存此user物件 
        session['username'] = empname  #將使用者姓名放入對話中
        return render_template('login_success.html', username=empname)
    else:
        return render_template('login_fail.html')
    
#---------------------------
# 登出
#---------------------------
@user_bp.route('/logout', methods=['GET'])
def logout():        
    logout_user()   #(登入管理)從session清除user物件
    session['username'] = None  #將使用者姓名從對話清除
    return render_template('logout.html')  
