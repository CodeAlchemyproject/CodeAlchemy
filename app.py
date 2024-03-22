#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session,request, jsonify
import subprocess
import math
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
def get_data(state,onlinejudge,difficulty,search):
    #取得資料庫連線 
    connection = db.get_connection() 
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()
    # 這裡加篩選條件
    cursor.execute('SELECT * FROM problem')
    #取出資料
    data = cursor.fetchall()    
    #關閉資料庫連線    
    connection.close()
    print(state,onlinejudge,difficulty,search)
    return data

#分頁功能
def paginate(state,onlinejudge,difficulty,search,page, per_page):
    offset = (page - 1) * per_page
    data=get_data(state,onlinejudge,difficulty,search)
    return data[offset: offset + per_page],len(data)

#主畫面
@app.route('/', methods=['GET'])
def index():
    # 取得使用者的篩選條件
    state = request.args.get('state','*',type=str)
    onlinejudge = request.args.get('onlinejudge','*',type=str)
    difficulty = request.args.get('difficulty','*',type=str)
    search = request.args.get('search','*',type=str)
    # 預設第一頁
    page = request.args.get('page', 1, type=int)
    # 每頁顯示15列
    per_page = 15
    start_page = max(1, page - 3)
    end_page = min(page+3,math.ceil(paginate(state,onlinejudge,difficulty,search,page, per_page)[1]/per_page)+1)
    paginated_data = paginate(state,onlinejudge,difficulty,search,page, per_page)[0]
    #渲染網頁
    return render_template('problem_list.html', data=paginated_data,page=page,start_page=start_page,end_page=end_page,state=state,onlinejudge=onlinejudge,difficulty=difficulty,search=search)
    
#題目
@app.route('/problem')
def problem():
    return render_template('./problem.html')
# 登入
@app.route('/login')
def login():
    return render_template('./login.html')

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