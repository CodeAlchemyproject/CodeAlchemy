# 匯入Blueprint模組
from flask import request, render_template, redirect, url_for
from flask_login import login_required
from flask import Blueprint
import os
import uuid

from utils import db
from utils import common

# 產生客戶服務藍圖
contest_bp = Blueprint('contest_bp', __name__)

#--------------------------
# 在客戶服務藍圖加入路由
#--------------------------
#員工新增表單
@contest_bp.route('/create/form')
def contest_create_form():
    return render_template('create_contest.html') 

#員工新增
@contest_bp.route('/create', methods=['POST'])
def contest_create():
    try:
        # 从表单中获取数据
        contest_name = request.form['contest_name']
        start_date = request.form['startTime']
        end_date = request.form['endTime']
        description = request.form['description']
        type = request.form['description']
        #print("Received contest name:", contest_name)
        #print("Received description:", description)


        # 获取数据库连接
        connection = db.connection()

        # 使用 SQL 插入数据到 'contest' 数据表
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contest (contest_name, start_date, end_date, description, type) VALUES (%s, %s, %s, %s, %s)",
                    (contest_name, start_date, end_date, description, type))

        # 提交更改
        connection.commit()

        # 若成功取得数据，重定向到问题列表页面
        return render_template('create_contest_success.html')
    except Exception as e:
        # 若发生错误，打印错误信息并返回创建失败页面
        print("Error occurred:", e)
        #return render_template('login.html', error=str(e))
    finally:
        # 关闭数据库连接
        connection.close()


#contest_list
@contest_bp.route('/join/form')
def contest_join(): 
  
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    cursor.execute("SELECT contest_name, description FROM contest")
    contests = cursor.fetchall()

    # close db conn
    conn.close()

    # 渲染 join_contest.html 
    return render_template('join_contest.html', contests=contests)
