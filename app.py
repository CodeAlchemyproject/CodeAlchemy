#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session
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
# 啟動主程式
#-------------------------
if __name__ == '__main__':
    app.run(debug=True)