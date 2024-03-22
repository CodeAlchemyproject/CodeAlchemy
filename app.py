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

#分頁功能
def paginate(page, per_page):
    offset = (page - 1) * per_page
    #取得資料庫連線 
    connection = db.get_connection() 
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT * FROM problem')
    #取出資料
    data = cursor.fetchall()    
    #關閉資料庫連線    
    connection.close()
    return data[offset: offset + per_page],len(data)

#主畫面
@app.route('/', methods=['GET'])
def index():
    # 預設第一頁
    page = request.args.get('page', 1, type=int)
    # 每頁顯示15列
    per_page = 15
    start_page = max(1, page - 3)
    end_page = min(page+3,math.ceil(paginate(page, per_page)[1]/per_page)+1)
    paginated_data = paginate(page, per_page)[0]

    state = request.args.get('state','none',type=str)
    onlinejudge = request.args.get('onlinejudge','none',type=str)
    difficulty = request.args.get('difficulty','none',type=str)
    print(state,onlinejudge,difficulty)
    #渲染網頁
    return render_template('problem_list.html', data=paginated_data,page=page,start_page=start_page,end_page=end_page,state=state,onlinejudge=onlinejudge,difficulty=difficulty)
    
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