#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session,request, jsonify
import subprocess
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

#主畫面
@app.route('/')
def index():

#取得資料庫連線 
    connection = db.get_connection() 
            
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT * FROM problem')
            
    #取出資料
    data = cursor.fetchall()    
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('problem_list.html', data=data)
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