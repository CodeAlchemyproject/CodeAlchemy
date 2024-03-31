# 匯入Blueprint模組
from flask import request, render_template
from flask_login import login_required
from flask import Blueprint
import os
import uuid

from . import db
from utils import common

# 產生客戶服務藍圖
customer_bp = Blueprint('customer_bp', __name__)

#--------------------------
# 在客戶服務藍圖加入路由
#--------------------------
#客戶清單
@customer_bp.route('/list')
@login_required
def customer_list(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT * FROM customer order by cusno')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close() 
    
    #渲染網頁  
    return render_template('customer_list.html', data=data)


#客戶查詢表單
@customer_bp.route('/read/form')
def customer_read_form():
    return render_template('customer_read_form.html') 


#客戶查詢
@customer_bp.route('/read', methods=['GET'])
def customer_read():    
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    cusno = request.values.get('cusno').strip().upper()
      
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('customer_read.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#客戶新增表單
@customer_bp.route('/create/form')
def customer_create_form():
    return render_template('customer_create_form.html') 


#客戶新增
@customer_bp.route('/create', methods=['POST'])
def customer_create():
    try:
        #取得上傳圖檔
        photo = request.files['photo']
        filename = None
        
        #檢查是否有選擇圖片, 並且檔案類型允可
        if photo and common.allowed_file(photo.filename):
            #產生一個唯一的檔名並儲存它
            filename = str(uuid.uuid4()) + '.' + photo.filename.rsplit('.', 1)[1].lower()
            photo.save(os.path.join('static/photos', filename))        
        
        #取得其他參數
        cusno = request.form.get('cusno').strip().upper()
        cusname = request.form.get('cusname')
        address = request.form.get('address')
        
        print(cusno, cusname, address)

        #取得資料庫連線
        conn = db.get_connection()

        #將資料加入customer表
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (cusno, cusname, address, photo) VALUES (%s, %s, %s, %s)",
                        (cusno, cusname, address, filename))
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('create_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('create_fail.html')

    
#客戶刪除表單
@customer_bp.route('/delete/form')
def customer_delete_form():
    return render_template('customer_delete_form.html') 


#客戶刪除確認
@customer_bp.route('/delete/confirm', methods=['GET'])
def customer_delete_confirm():
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    cusno = request.values.get('cusno').strip().upper()
      
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('customer_delete_confirm.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#客戶刪除
@customer_bp.route('/delete', methods=['POST'])
def customer_delete():
    try:
        #取得參數
        cusno = request.form.get('cusno').strip().upper()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料從customer表刪除
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customer WHERE cusno = %s", (cusno,))
        
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('delete_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('delete_fail.html')    

    
#客戶更改表單
@customer_bp.route('/update/form')
def customer_update_form():
    return render_template('customer_update_form.html') 


#客戶更改確認
@customer_bp.route('/update/confirm', methods=['GET'])
def customer_update_confirm():
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數, 執行sql命令並取回資料  
    cusno = request.values.get('cusno').strip().upper()
      
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    #關閉連線   
    connection.close()  
        
    #渲染網頁
    if data:
        return render_template('customer_update_confirm.html', data=data) 
    else:
        return render_template('not_found.html')
    
    
#客戶更改
@customer_bp.route('/update', methods=['POST'])
def customer_update():
    try:
        #取得參數
        cusno = request.form.get('cusno')
        cusname = request.form.get('cusname')
        address = request.form.get('address')

        #取得資料庫連線
        conn = db.get_connection()

        #將資料從customer表刪除
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET cusname=%s, address=%s WHERE cusno = %s", (cusname, address, cusno))
        
        conn.commit()
        conn.close()

        # 渲染成功畫面
        return render_template('update_success.html')
    except Exception as e:
        #印出錯誤原因
        print('-'*30)
        print(e)
        print('-'*30)
        
        # 渲染失敗畫面
        return render_template('update_fail.html')      