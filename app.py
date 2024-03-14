#-----------------------
# 匯入模組
#-----------------------
from flask import Flask, render_template, session,request, jsonify
import subprocess
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
            return render_template('problem_list.html', name=session['username']) 
        else:
            return render_template('problem_list.html', name='尚未登入')
    except:
        return render_template('problem_list.html', name='尚未登入')
#題目
@app.route('/problem')
def problem():
    return render_template('./problem.html')
# 登入
@app.route('/login')
@app.route('/run_code', methods=['POST'])
def run_code():
    # 獲取前端傳遞的程式碼和語言
    user_code = request.json.get('code')
    language = request.json.get('language')

    # 設置預設結果
    result = "沒有結果"

    # 執行不同語言的程式碼
    if language == 'C':
        result = execute_c_code(user_code)
    elif language == 'C++':
        result = execute_cpp_code(user_code)
    elif language == 'Java':
        result = execute_java_code(user_code)

    # 返回執行結果給前端
    return jsonify({'result': result})

def execute_c_code(code):
    # 編譯並執行 C 程式碼
    try:
        compiled_code = subprocess.check_output(['gcc', '-xc', '-', '-o', 'temp_c'], input=code, stderr=subprocess.STDOUT, universal_newlines=True)
        executed_code = subprocess.check_output(['./temp_c'], stderr=subprocess.STDOUT, universal_newlines=True)
        return executed_code
    except subprocess.CalledProcessError as e:
        return f"發生錯誤：{e.output}"

def execute_cpp_code(code):
    # 編譯並執行 C++ 程式碼
    try:
        compiled_code = subprocess.check_output(['g++', '-xc++', '-', '-o', 'temp_cpp'], input=code, stderr=subprocess.STDOUT, universal_newlines=True)
        executed_code = subprocess.check_output(['./temp_cpp'], stderr=subprocess.STDOUT, universal_newlines=True)
        return executed_code
    except subprocess.CalledProcessError as e:
        return f"發生錯誤：{e.output}"

def execute_java_code(code):
    # 編譯並執行 Java 程式碼
    try:
        compiled_code = subprocess.check_output(['javac', '-'], input=code, stderr=subprocess.STDOUT, universal_newlines=True)
        executed_code = subprocess.check_output(['java', 'Main'], stderr=subprocess.STDOUT, universal_newlines=True)
        return executed_code
    except subprocess.CalledProcessError as e:
        return f"發生錯誤：{e.output}"


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