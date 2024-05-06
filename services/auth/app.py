from flask import Flask,Blueprint,render_template,session,request,url_for,redirect,make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
# google登入
from authlib.integrations.flask_client import OAuth
# google憑證金鑰
from config import GOOGLE_CELENT_ID,GOOGLE_CELENT_SERRET
#驗證信模組
from flask_mail import Mail, Message
from config import MAIL_PASSWORD,MAIL_USERNAME
# 匯入其他藍圖
from utils import db

app=Flask(__name__)
auth_bp = Blueprint('auth', __name__)
# 傳送驗證電子郵件
app.config['SECRET_KEY'] = 'itismysecretkey'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail =Mail(app)
# google登入
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CELENT_ID,
    client_secret=GOOGLE_CELENT_SERRET,
    client_kwargs= {"scope": "openid email profile"},
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration')

# 查詢電子郵件有沒有註冊過
@auth_bp.route('/login',methods=['GET','POST'])
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
            return redirect('/auth/login_password')
        # 如果沒有註冊過跳轉到註冊頁面
        else:
            return redirect('/auth/register')
    else:
        return render_template('login.html')
# google 登入
@auth_bp.route('/google')
def login_google():
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/google-callback')
def authorize():
    # 使用?取的??令牌??取用?的信息
    token = google.authorize_access_token()
    user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    print(user_info)
    Goole_ID=user_info['id']
    Email = user_info['email']
    imgs = user_info['picture']
    sql_user_command=f"SELECT * FROM user where email='{Email}'"
    user_data=db.get_data(sql_user_command)
    # 如果有用email註冊過
    if len(user_data) == 1:
        # 將使用者資料存入session
        session['Email'] = Email
        session['logged_in']=True
        session['User_name']=user_data[0][1]
        session['google_id']=Goole_ID
        session['imgs']=imgs
        if user_data[0][3]==Goole_ID:
            return redirect('/')
        else:
            return redirect('/auth/connect_google')
    # 在這裡處理使用者資訊，例如驗證、註冊等等
    else:
        return redirect('/auth/register')
@auth_bp.route('/connect_google',methods=['GET','POST'])
def connect_google():
    google_id=session.get('google_id')
    Email = session.get('Email')
    imgs = session.get('imgs')
    if request.method=="POST":
        Password=request.form['Password']
        sql_common=f"SELECT * FROM user where email='{Email}'"
        user_data=db.get_data(sql_common)
        # 認證成功
        if check_password_hash(db.get_data(sql_common)[0][2],Password):
            session['logged_in']=True
            session['User_name']=user_data[0][1]
            session['User_id']=user_data[0][0]
            sql_user_command=f"UPDATE user SET google_id ='{google_id}',image='{imgs}' where email='{Email}'"
            db.edit_data(sql_user_command)
            return redirect('/')
        else:
            result='密碼錯誤'
            return render_template('connect_google.html',result=result)
    return render_template('connect_google.html')
# 輸入密碼
@auth_bp.route('/login_password',methods=['GET','POST'])
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
        # 取得使用者資料
        sql_common=f"SELECT * FROM user where email='{Email}'"
        user_data=db.get_data(sql_common)
        # 登入成功
        if check_password_hash(db.get_data(sql_common)[0][2],Password):
            session['logged_in']=True
            session['User_name']=user_data[0][1]
            session['User_id']=user_data[0][0]
            # 如果使用者有勾記住我
            if Rememberme==1:
                resp = make_response(redirect('/'))
                # cookie效期30天
                resp.set_cookie('logged_in','True',max_age=60*60*24*30)
                resp.set_cookie('user_name',user_data[0][1],max_age=60*60*24*30)
                resp.set_cookie('user_id',str(user_data[0][0]),max_age=60*60*24*30)
                return resp
            else:
                return redirect('/')
        # 密碼錯誤登入失敗
        else:
            result='密碼錯誤'
            return render_template('login_password.html',result=result)
    else:
        return render_template('login_password.html')
# 註冊
@auth_bp.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == "POST":
        user_name=request.form['Username']
        Email=request.form['Email']
        Password=request.form['Password']
        if db.get_data(f"SELECT * FROM user where email='{Email}'"):
            result='此Email已經註冊過'
            return redirect('/auth/login')
        else:
            token=str(uuid.uuid4())
            sql_user_command=f"INSERT INTO user(user_name,password,email,permission,uuid) VALUES ('{user_name}','{generate_password_hash(Password)}','{Email}','Default user','{token}')"
            db.edit_data(sql_user_command)
            html=f'http://140.131.114.141/auth/verify_register?uuid={token}'
            msg_title = 'Welcome to CodeAlchemy'
            msg_recipients=[Email]
            msg_html =f'<p>親愛的 {user_name}，<br>感謝您註冊成為我們平台的一員！為了確保您的帳戶安全，請點擊以下連結驗證您的電子郵件地址：<a href="{html}">驗證連結</a>。<br>如果您無法點擊上述連結，請將以下網址複製並粘貼到瀏覽器地址欄中：<a href="{html}">{html}</a>。<br>請完成這一步驟以啟用您的帳戶。如果您遇到任何問題或需要協助，請隨時聯繫我們的客戶服務團隊，我們將竭誠為您服務。<br>謝謝您的合作！<br>祝您有個愉快的體驗！</p>'
            msg = Message(
                subject=msg_title,
                sender = 'codealchemyproject@gmail.com',
                recipients=msg_recipients,
                html=msg_html,
                charset='UTF-8'
            )
            mail.send(msg)
            result='註冊成功'
        return render_template('register_result.html',result=result)
    else:
        return render_template('register.html')
# 忘記密碼
@auth_bp.route('/forget_password' ,methods=['GET','POST'])
def forget_password():
    if request.method == "POST":
        Email=request.form['Email']
        user_name=db.get_data(f"SELECT * FROM user where email='{Email}'")[0][1]
        token=str(uuid.uuid4())
        db.edit_data(f"UPDATE user SET uuid = '{token}' WHERE email='{Email}'")
        html=f'http://140.131.114.141/auth/verify_forget_password?uuid={token}'
        msg_title = 'Forget CodeAlchemy Password'
        msg_recipients=[Email]
        msg_html =f'<p>親愛的{user_name},</p><p>我們注意到您最近嘗試登入您的帳號時遇到了一些問題。如果您忘記了您的密碼，請不要擔心，我們很樂意協助您重設密碼。</p><p>請點擊以下連結以重設您的密碼：</p><a href="{html}">重設密碼</a><p>如果點擊上述連結無法正常工作，請複製並粘貼以下網址至您的瀏覽器中：</p><p>{html}</p><p>請注意，此連結將在收到此郵件後的24小時內有效。請盡快完成密碼重設流程。</p><p>如果您沒有請求重設密碼，請忽略此郵件。您的帳號安全是我們的首要關注。</p><p>如果您有任何疑問或需要進一步協助，請隨時回覆此郵件與我們聯繫。</p>'.encode('utf-8')
        msg = Message(
            subject=msg_title,
            sender = 'codealchemyproject@gmail.com',
            recipients=msg_recipients,
            html=msg_html
        )
        mail.send(msg)
        return redirect('/auth/login')
    else:
        return render_template('forget_password.html')
# 註冊驗證
@auth_bp.route('/verify_register',methods=['GET'])
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
        return render_template('verify_register.html',result=result)
    else:
        result='驗證失敗'
        return render_template('verify_register.html',result=result)
# 忘記密碼驗證
@auth_bp.route('/verify_forget_password',methods=['GET','POST'])
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
            return render_template('verify_forget_password_result.html',result=result)
        else:
            return render_template('verify_forget_password.html',uuid=uuid)
    else:
        result='錯誤'
        return render_template('verify_forget_password_result.html',result=result)
#更改密碼
@auth_bp.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method == "POST":
        Email=session.get('Email')
        sql_common=f"SELECT * FROM user where email='{Email}'"
        oldPassword=request.form['oldPassword']
        newPassword=request.form['newPassword']
        renewPassword=request.form['renewPassword']
        # 檢查密碼一致性
        if newPassword==renewPassword:
            # 新密碼加密
            newPassword=generate_password_hash(newPassword)
            # 檢查舊密碼
            if check_password_hash(db.get_data(sql_common)[0][2],oldPassword):
                sql_common= f"UPDATE user SET password = '{newPassword}' WHERE email='{Email}'"
                db.edit_data(sql_common)
                return render_template('change_password_success.html')
            else:
                result='密碼錯誤'
                return render_template('change_password.html',result=result)
        else:
            result='密碼不一致'
            return render_template('change_password.html',result=result)
    else:
        return render_template('change_password.html')
#登出 
@auth_bp.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect('/'))
    resp.set_cookie('logged_in','',expires=0)
    resp.set_cookie('user_name','',expires=0)
    resp.set_cookie('user_id','',expires=0)
    return resp