#-----------------------
# 匯入模組
#-----------------------
from flask import Flask,render_template,session,request,redirect
import subprocess
import math
import time
#-----------------------
# 匯入各個服務藍圖
#-----------------------
from services.customer.app import customer_bp
from services.problem.app import problem_bp
from services.user.app import user_bp, login_manager
from utils import db, common
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
    start_page = max(1, page - 3)
    end_page = min(page+3,math.ceil(paginate(data,page, per_page)[1]/per_page)+1)
    paginated_data = paginate(data,page, per_page)[0]
    print(session.get('logged_in'))
    #渲染網頁
    return render_template('problem_list.html', session=session,data=paginated_data,page=page,start_page=start_page,end_page=end_page,state=state,onlinejudge=onlinejudge,difficulty=difficulty,search=search)
@app.route('/navbar', methods=['GET'])
def navbar():
    session
#題目
@app.route('/problem',methods=['GET'])
def problem():
    problem_id = request.args.get('problem_id',type=str)
    sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
    data=get_data(sql_problem_command)
    print(data)
    return render_template('./problem.html',data=data)


# 登入
@app.route('/login',methods=['GET','POST'])
def login():
    # 收到登入資料
    if request.method=="POST":
        Email=request.form['Email']
        password=request.form['Password']
        sql_common=f"SELECT * FROM [user] where email='{Email}'"
        # 如果有註冊過
        user_data=get_data(sql_common)
        if len(user_data)==1:
            # 登入成功
            if user_data[0][2]==password:
                session['logged_in']=True
                session['User_name']=user_data[0][1]
                return redirect('/')
            # 帳號密碼錯誤登入失敗
            else:
                print('登入失敗')
            return render_template('./login.html')
        # 如果沒有註冊過
        else:
            return redirect('/register')
    else:
        return render_template('./login.html')
# 註冊
@app.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == "POST":
        user_name=request.form['Username']
        Email=request.form['Email']
        Password=request.form['Password']
        if get_data(f"SELECT * FROM [user] where email='{Email}'"):
            result='此Email已經註冊過'
            time.sleep(3)
            return redirect('/login')
        else:
            sql_user_commond=f"INSERT INTO [user](user_name,password,email) VALUES ('{user_name}','{Password}','{Email}')"
            insert_data(sql_user_commond)
            result='註冊成功'
        return render_template('./register_result.html',result=result)
    else:
        return render_template('./register.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(user_bp, url_prefix='/user')  
app.register_blueprint(problem_bp, url_prefix='/problem') 
login_manager.init_app(app)  

#-------------------------
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(debug=True)