# 匯入Blueprint模組
from flask import request, render_template
from flask_login import login_required
from flask import Blueprint
import os


from utils import db, common

# 產生客戶服務藍圖
problem_bp = Blueprint('problem_bp', __name__)
#--------------------------
# 在客戶服務藍圖加入路由
#--------------------------
#題目清單
@problem_bp.route('/list')
#@login_required
def problem_list(): 
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
    return render_template('[problem_list.html', data=data)
