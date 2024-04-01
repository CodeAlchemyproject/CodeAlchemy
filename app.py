#-----------------------
# 匯入模組
#-----------------------
from flask import Flask,render_template,session,request,redirect,make_response
from flask_mail import Mail,Message
import subprocess
import math
import time
from werkzeug.security import generate_password_hash,check_password_hash
#-----------------------
# 匯入各個服務藍圖
#-----------------------
from utils import db
from services.customer.app import customer_bp
from services.problem.app import problem_bp
from services.user.app import user_bp, login_manager
from utils import common
#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

#加密(登入/登出)
app.config['SECRET_KEY'] = 'itismysecretkey'

#取得並篩選資料
def get_data(sql_command):
    #取得資料庫連線 
    connection = db.get_connection() 
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()
    # 這裡加篩選條件
    cursor.execute(sql_command)
    #取出資料
    data = cursor.fetchall()    
    #關閉資料庫連線    
    connection.close()
    return data

#新增資料
def insert_data(sql_commond):
    #取得資料庫連線 
    connection = db.get_connection() 
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()
    # 這裡加篩選條件
    cursor.execute(sql_commond)
    connection.commit()
    #關閉資料庫連線    
    connection.close()

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
    data=get_data(sql_problem_command)
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
    data=get_data(sql_problem_command)
    return render_template('./problem.html',data=data)

# 查詢電子郵件有沒有註冊過
@app.route('/login',methods=['GET','POST'])
def login():
    # 收到電子郵件
    if request.method=="POST":
        Email=request.form['Email']
        sql_common=f"SELECT * FROM [user] where email='{Email}'"
        # 如果有註冊過
        user_data=get_data(sql_common)
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
        sql_common=f"SELECT * FROM [user] where email='{Email}'"
        user_data=get_data(sql_common)
        # 登入成功
        if check_password_hash(get_data(sql_common)[0][2],Password):
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
        if get_data(f"SELECT * FROM [user] where email='{Email}'"):
            result='此Email已經註冊過'
            return redirect('/login')
        else:
            print(generate_password_hash(Password))
            # sql_user_commond=f"INSERT INTO [user](user_name,password,email) VALUES ('{user_name}','{generate_password_hash(Password)}','{Email}')"
            # insert_data(sql_user_commond)
            result='註冊成功'
            msg_title = 'Hello'
            msg_recipients=[Email]
            msg_html = '這是 flask-mail example <br> <br>' \
                    '附上一張圖片 <br> <br>' \
                    '<b  style="color:#FF4E4E" >新垣結衣</b>'
            msg = Message(
                subject=msg_title,
                sender = 'codealchemyproject@gmail.com',
                recipients=msg_recipients,
                html=msg_html
            )
            mail.send(msg)
        return render_template('./register_result.html',result=result)
    else:
        return render_template('./register.html')
#登出 
@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect('/'))
    resp.set_cookie('logged_in','',expires=0)
    resp.set_cookie('user_name','',expires=0)
    return resp

@app.route('/send-email')
def send_mail():
    msg_title = 'Hello'
    msg_recipients=['chouenyu940808@gmail.com']
    msg_html = '這是 flask-mail example <br> <br>' \
              '附上一張圖片 <br> <br>' \
              '<b  style="color:#FF4E4E" >新垣結衣</b>'
    msg = Message(
        subject=msg_title,
        sender = 'codealchemyproject@gmail.com',
        recipients=msg_recipients,
        html=msg_html
    )
    # msg.body = '純文字'
    # msg.html=msg_html
    mail.send(msg)
    return()
@app.route('/user_data')
def user_data():
    return render_template('./user_data.html')
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