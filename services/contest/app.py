# 匯入Blueprint模組
from flask import request, render_template, jsonify, json
import sqlite3
from flask import Blueprint


from utils import db
from utils.common import paginate

# 產生contest服務藍圖
contest_bp = Blueprint('contest_bp', __name__)

#--------------------------
# 在contest服務藍圖加入路由
#--------------------------


#contest create form
@contest_bp.route('/create/form')
def contest_create_form():
    return render_template('create_contest.html') 


#create contest
@contest_bp.route('/create', methods=['POST'])
def contest_create():
    try:
        # 從表單獲取數據
        contest_name = request.form['contest_name']
        start_date = request.form['startTime']
        end_date = request.form['endTime']
        description = request.form['description']
        type = request.form['description']
        #print("Received contest name:", contest_name)
        #print("Received description:", description)


        # 資料庫連接
        connection = db.connection()

        # 新增到contest資料表
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contest (contest_name, start_date, end_date, description, type) VALUES (%s, %s, %s, %s, %s)",
                    (contest_name, start_date, end_date, description, type))

        # 提交更改
        connection.commit()

        # 若成功取得數據，導向create_contest_success.html
        return render_template('create_contest_success.html')
    except Exception as e:
        # 若發生錯誤，導向失敗頁面
        print("Error occurred:", e)
        #return render_template('login.html', error=str(e))
    finally:
        # 關閉資料庫連接
        connection.close()



#contest_list
@contest_bp.route('/join/form')
def contest_join(): 
  
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    cursor.execute("SELECT contest_name, start_date, end_date, description, type FROM contest")
    contests = cursor.fetchall()

    # close db conn
    conn.close()

    # 渲染 join_contest.html 
    return render_template('join_contest_form.html', contests=contests)


'''
@contest_bp.route('/get_problems')
#def get_problems():
#    return jsonify(mock_db)
def get_problems():
    # 连接到您的数据库（这里假设数据库的名字是database.db）
    conn = db.connection()
    cur = conn.cursor()
    
    # 执行查询操作
    cur.execute("SELECT title, content, difficulty FROM problem")
    problems_data = cur.fetchall()
    
    # 关闭连接
    cur.close()
    conn.close()
  
    # 返回查询结果给前端
    return jsonify(problems_data)
    
'''

@contest_bp.route('/get_problems')
def get_problems():
    # 获取URL参数中的page和per_page变量，如果没有则分别默认为1和10
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # 建立到数据库的连接
    conn = db.connection()
    cur = conn.cursor()
    
    # 计算应该跳过的记录数
    offset = (page - 1) * per_page
    # 执行分页查询
    cur.execute("SELECT title, content, difficulty FROM problem LIMIT %s OFFSET %s;", (per_page, offset))
    problems_data = cur.fetchall()
    
    # 获取数据库中题目的总数以计算页数
    cur.execute("SELECT COUNT(*) FROM problem;")
    total_problems = cur.fetchone()[0]
    total_pages = (total_problems + per_page - 1) // per_page  # 计算总分页数
    
    # 关闭连接
    cur.close()
    conn.close()
  
    # 返回查询结果给前端，附加分页信息
    return jsonify({
        'data': problems_data,
        'total': total_problems,
        'page': page,
        'total_pages': total_pages,
        'per_page': per_page
    })


