#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session

#-----------------------
# 匯入各個服務藍圖
#-----------------------
from services.customer.app import customer_bp
from services.user.app import user_bp, login_manager

#-------------------------
# 產生主程式, 加入主畫面
#-------------------------
app = Flask(__name__)

#加密(登入/登出)
app.config['SECRET_KEY'] = 'itismysecretkey'

#主畫面
@app.route('/')
def index():
    try:
        if session['username']:
            return render_template('index.html', name=session['username']) 
        else:
            return render_template('index.html', name='尚未登入')
    except:
        return render_template('index.html', name='尚未登入')

#-------------------------
# 在主程式註冊各個服務
#-------------------------
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(user_bp, url_prefix='/user')  
login_manager.init_app(app)  

#-------------------------
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(debug=True)