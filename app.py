#-----------------------
# 匯入模組
#-----------------------
import os
import threading
from flask import Flask, json,render_template,session,request,redirect,make_response,jsonify, url_for
from flask_mail import Mail,Message
import subprocess
import math
import time
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
from queue import Queue
#-----------------------
# 匯入各個服務藍圖
#-----------------------

from services.customer.app import customer_bp
from services.problem.app import problem_bp
from services.user.app import user_bp, login_manager
from utils import db,common
from 爬蟲.ZJ_submit import process_account

#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

#加密(登入/登出)
app.config['SECRET_KEY'] = 'itismysecretkey'


#分頁功能
def paginate(data,page, per_page):
    offset = (page - 1) * per_page
    return data[offset: offset + per_page],len(data)

# 傳送驗證電子郵件
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codealchemyproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'zsog pref sqoh xagd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
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

    # 輸出每個變數的值
    print("Type:", type)
    print("Problem ID:", problem_id)
    print("Language:", language)
    print("Code:", code)
    
    # 定義語言對應的文件擴展名字典
    file_extensions = {
        'python': '.py',
        'java': '.java',
        'c': '.c',
        'cpp': '.cpp'
    }
    problem_id = problem_id.split('-')[1]
    # 構建文件路徑
    file_path = os.path.join('./source', f'{problem_id}{file_extensions[language]}')

    # 確保目錄存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 寫入內容到文件中
    with open(file_path, 'w') as file:
        file.write(code)

    # 假設有三個目標文件夾
    target_folders = ['./爬蟲/src/BeAPro113', './爬蟲/src/TestCase2024', './爬蟲/src/yyyiii']

    # 將文件分配到目標文件夾中
    common.distribute_files('./source', target_folders)

    # 讀取帳戶資訊
    with open('./爬蟲/account.json', 'r') as file: 
        accounts = json.load(file)['account']

    # 多執行序
    threads = []
    for acc in accounts:
        username = acc[0]
        password = acc[1]
        # 構建該使用者資料夾的路徑
        user_folder_path = os.path.join('./爬蟲/src/', username)
        # 檢查該資料夾是否存在並且是否為空
        if os.path.exists(user_folder_path) and os.listdir(user_folder_path):
            # 如果該資料夾存在並且不為空，則進行處理
            # 將該使用者資料夾下的檔案加入執行序中
            for file_name in os.listdir(user_folder_path):
                file_path = os.path.join(user_folder_path, file_name)
                if os.path.isfile(file_path):
                    
                    thread = threading.Thread(target=process_account, args=(username, password, language))
                    threads.append(thread)
                    thread.start()
        else:
            # 如果該資料夾不存在或者為空，則顯示相應的訊息
            print(f"資料夾 {username} 為空，未加入執行序。")

    # 等待所有執行序完成
    for thread in threads:
        thread.join()
    return jsonify({'success': True})

# 查詢電子郵件有沒有註冊過
@app.route('/login',methods=['GET','POST'])
def login():
    # 收到電子郵件
    if request.method=="POST":
        Email=request.form['Email']
        sql_user_command=f"SELECT * FROM user where email='{Email}'"
        user_data=db.get_data(sql_user_command)
        # 如果有註冊過
        if len(user_data) == 1:
            # 將Email存入session
            session['Email'] = Email
            return redirect('/login_password')
        # 如果沒有註冊過跳轉到註冊頁面
        else:
            return redirect('/register')
    else:
        return render_template('./login.html')
# 輸入密碼
@app.route('/login_password',methods=['GET','POST'])
def login_password():
    # 收到密碼
    if request.method=="POST":
        Email = session.get('Email')
        Password=request.form['Password']
        # 記住我
        try:
            Rememberme=request.form['Rememberme']
            Rememberme=1
        except Exception:
            Rememberme=0
        # 取的使用者資料
        sql_common=f"SELECT * FROM user where email='{Email}'"
        user_data=db.get_data(sql_common)
        # 登入成功
        if check_password_hash(db.get_data(sql_common)[0][2],Password):
            session['logged_in']=True
            session['User_name']=user_data[0][1]
            # 如果使用者有勾記住我
            if Rememberme==1:
                resp = make_response(redirect('/'))
                # cookie效期30天
                resp.set_cookie('logged_in','True',max_age=60*60*24*30)
                resp.set_cookie('user_name',user_data[0][1],max_age=60*60*24*30)
                return resp
            else:
                return redirect('/')
        # 密碼錯誤登入失敗
        else:
            result='密碼錯誤'
            return render_template('./login_password.html',result=result)
    else:
        return render_template('./login_password.html')
# 註冊
@app.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == "POST":
        user_name=request.form['Username']
        Email=request.form['Email']
        Password=request.form['Password']
        if db.get_data(f"SELECT * FROM user where email='{Email}'"):
            result='此Email已經註冊過'
            return redirect('/login')
        else:
            token=str(uuid.uuid4())
            sql_user_command=f"INSERT INTO user(user_name,password,email,permission,uuid) VALUES ('{user_name}','{generate_password_hash(Password)}','{Email}','Default user','{token}')"
            db.edit_data(sql_user_command)
            html=f'http://140.131.114.141/verify_register?uuid={token}'
            msg_title = 'Welcome to CodeAlchemy'
            msg_recipients=[Email]
            msg_html =f'<p>親愛的 {user_name}，<br>感謝您註冊成為我們平台的一員！為了確保您的帳戶安全，請點擊以下連結驗證您的電子郵件地址：<a href="{html}">驗證連結</a>。<br>如果您無法點擊上述連結，請將以下網址複製並粘貼到瀏覽器地址欄中：<a href="{html}">{html}</a>。<br>請完成這一步驟以啟用您的帳戶。如果您遇到任何問題或需要協助，請隨時聯繫我們的客戶服務團隊，我們將竭誠為您服務。<br>謝謝您的合作！<br>祝您有個愉快的體驗！</p>'
            msg = Message(
                subject=msg_title,
                sender = 'codealchemyproject@gmail.com',
                recipients=msg_recipients,
                html=msg_html
            )
            mail.send(msg)
            result='註冊成功'
        return render_template('./register_result.html',result=result)
    else:
        return render_template('./register.html')
# 忘記密碼
@app.route('/forget_password' ,methods=['GET','POST'])
def forget_password():
    if request.method == "POST":
        Email=request.form['Email']
        user_name=db.get_data(f"SELECT * FROM user where email='{Email}'")[0][1]
        token=str(uuid.uuid4())
        db.edit_data(f"UPDATE user SET uuid = '{token}' WHERE email='{Email}'")
        html=f'http://140.131.114.141/verify_forget_password?uuid={token}'
        msg_title = 'Forget CodeAlchemy Password'
        msg_recipients=[Email]
        msg_html =f'<p>親愛的{user_name},</p><p>我們注意到您最近嘗試登入您的帳號時遇到了一些問題。如果您忘記了您的密碼，請不要擔心，我們很樂意協助您重設密碼。</p><p>請點擊以下連結以重設您的密碼：</p><a href="{html}">重設密碼</a><p>如果點擊上述連結無法正常工作，請複製並粘貼以下網址至您的瀏覽器中：</p><p>{html}</p><p>請注意，此連結將在收到此郵件後的24小時內有效。請盡快完成密碼重設流程。</p><p>如果您沒有請求重設密碼，請忽略此郵件。您的帳號安全是我們的首要關注。</p><p>如果您有任何疑問或需要進一步協助，請隨時回覆此郵件與我們聯繫。</p>'
        msg = Message(
            subject=msg_title,
            sender = 'codealchemyproject@gmail.com',
            recipients=msg_recipients,
            html=msg_html
        )
        mail.send(msg)
        return redirect('/login')
    else:
        return render_template('./forget_password.html')
# 註冊驗證
@app.route('/verify_register',methods=['GET'])
def verify_register():
    # 獲得uuid
    uuid = request.args.get('uuid',None,type=str)
    sql_command=f"SELECT * FROM user where uuid='{uuid}'"
    data=db.get_data(sql_command)
    if len(data)==1:
        sql_command = f"UPDATE user SET register_time = NOW() WHERE uuid='{uuid}'"
        db.edit_data(sql_command)
        sql_command = f"UPDATE user SET uuid = Null WHERE uuid='{uuid}'"
        db.edit_data(sql_command)
        result='驗證成功'
        return render_template('./verify_register.html',result=result)
    else:
        result='驗證失敗'
        return render_template('./verify_register.html',result=result)
# 忘記密碼驗證
@app.route('/verify_forget_password',methods=['GET','POST'])
def verify_forget_password():
    # 獲得UUID
    uuid = request.args.get('uuid',None,type=str)
    if request.method == "POST":
            uuid=request.form['uuid']
    # 檢查UUID是否存在
    sql_command=f"SELECT * FROM user where uuid='{uuid}'"
    data=db.get_data(sql_command)
    if len(data)==1:
        if request.method == "POST":
            uuid=request.form['uuid']
            Password=request.form['Password']
            Password=generate_password_hash(Password)
            sql_command = f"UPDATE user SET password = '{Password}' WHERE uuid='{uuid}'"
            db.edit_data(sql_command)
            sql_command = f"UPDATE user SET uuid = Null WHERE uuid='{uuid}'"
            db.edit_data(sql_command)
            result='變更成功'
            return render_template('./verify_forget_password_result.html',result=result)
        else:
            return render_template('./verify_forget_password.html',uuid=uuid)
    else:
        result='錯誤'
        return render_template('./verify_forget_password_result.html',result=result)
#登出 
@app.route('/logout')
def logout():
    # session.clear()
    resp = make_response(redirect('/'))
    resp.set_cookie('logged_in','',expires=0)
    resp.set_cookie('user_name','',expires=0)
    return resp


@app.route('/user_data',methods=['GET'])
def user_data():
    Email = session.get('Email')
    sql_command=f"SELECT * FROM user where email='{Email}'"
    data=db.get_data(sql_command)
    User_name=data[0][1]
    Email=data[0][3]
    img=data[0][4]
    register_time=data[0][5]
    return render_template('./user_data.html',User_name=User_name,Email=Email,img=img,register_time=register_time)

# #懸浮視窗按鈕處理
# @app.route('/redirect', methods=['POST'])
# def redirect():
#     choice = request.form['choice']
#     if choice == 'A':
#         return redirect(url_for('add_contest'))  # 跳到add_contest.html頁面
#     elif choice == 'B':
#         return redirect(url_for('create_contest'))  # 跳到create_contest.html頁面

# @app.route('/add_contest.html')
# def add_contest():
#     return render_template('add_contest.html')  # 返回add_contest.html頁面的内容

# @app.route('/create_contest.html')
# def create_contest():
#     return render_template('create_contest.html')  # 返回create_contest.html頁面的内容

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(user_bp, url_prefix='/user')  
app.register_blueprint(problem_bp, url_prefix='/problem') 
login_manager.init_app(app)  

#-------------------------
# 啟動主程式
#------------------------
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True)