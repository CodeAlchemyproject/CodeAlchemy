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

'''
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
'''


#contest_list
@contest_bp.route('/join/form')
def contest_join(): 
  
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    cursor.execute("SELECT contest_id, contest_name, start_date, end_date, description, type FROM contest")
    contests = cursor.fetchall()

    # close db conn
    conn.close()

    # 渲染 join_contest.html 
    return render_template('join_contest_form.html', contests=contests)

'''
@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    
    conn = db.connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT contest_name FROM contest WHERE contest_id = %s", (contest_id,))
    contest_name = cursor.fetchone()[0]
    
    conn.close()

    return render_template('contest_joined.html', contest_name=contest_name)
'''


@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    print("Received contest_id:", contest_id)  # 打印出來看看接收到的 contest_id
    
    conn = db.connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT contest_name FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()
    print("Query result:", result)  # 打印查詢結果，檢查是否為 None
    
    conn.close()
    
    if result is None:
        return "比賽不存在", 404
    
    contest_name = result[0]

    return render_template('contest_joined.html', contest_name=contest_name)




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
    cur.execute("SELECT problem_id, title, content, difficulty FROM problem LIMIT %s OFFSET %s;", (per_page, offset))
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



'''
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
'''


'''
# 路由：处理创建比赛的POST请求
@contest_bp.route('/create', methods=['POST'])
def create_contest():
    try:
        # 從表單獲取數據
        contest_name = request.form['contest_name']
        start_date = request.form['startTime']
        end_date = request.form['endTime']
        description = request.form['description']
        type = request.form['description']
        #print("Received contest name:", contest_name)
        print("Received start_date:", start_date)

        # 从表单数据中解析数据
        contest_data = request.form.to_dict()
        problem_ids = contest_data.get('problem_ids').split(',')
        print(problem_ids)

        # 資料庫連接
        connection = db.connection()

        # 新增到contest資料表
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contest (contest_name, start_date, end_date, description, type) VALUES (%s, %s, %s, %s, %s)",
                    (contest_name, start_date, end_date, description, type))
        
        # 提交更改
        #connection.commit()

        # 创建比赛并获取 contest_id
        contest_id = create_contest_in_db(contest_data)

        # 循环添加题目到 contest_problem 表
        for problem_id in problem_ids:
            connect_contest_and_problem(contest_id, problem_id)

        return render_template('create_contest_success.html')
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"status": "error", "message": contest_data.get('problem_ids')})
    finally:
        # 确保关闭数据库连接
        if 'connection' in locals():
            connection.close()

# 辅助函数：在数据库中创建比赛，并返回 contest_id
def create_contest_in_db(contest_data):
    connection = db.connection()
    cursor = connection.cursor()

    # 从 contest_data 字典中提取字段
    contest_name = contest_data.get('contest_name')
    start_date = contest_data.get('start_date')
    end_date = contest_data.get('end_date')
    description = contest_data.get('description')
    type = contest_data.get('type')

    #print(type)

    # 插入数据并返回 contest_id
    cursor.execute(
        "INSERT INTO contest (contest_name, start_date, end_date, description, type) VALUES (%s, %s, %s, %s, %s);",
        (contest_name, start_date, end_date, description, type)
    )  
    

    # 获取新插入记录的 contest_id
    contest_id = cursor.lastrowid

    connection.commit()
    cursor.close()
    connection.close()

    return contest_id

# 辅助函数：将 contest_id 和 problem_id 关联起来
def connect_contest_and_problem(contest_id, problem_id):
    connection = db.connection()
    cursor = connection.cursor()

    # 插入 contest_id 和 problem_id 到 contest_problem 表中
    cursor.execute(
        "INSERT INTO contest_problem (contest_id, problem_id) VALUES (%s, %s);",
        (contest_id, problem_id)
    )

    connection.commit()
    cursor.close()
    connection.close()
'''


# 路由：處理創建比賽的POST請求
@contest_bp.route('/create', methods=['POST'])
def create_contest():
    connection = None
    try:
        # 從表單取得數據
        contest_name = request.form.get('contest_name')
        start_date = request.form.get('startTime')
        end_date = request.form.get('endTime')
        description = request.form.get('description')
        type = request.form.get('description')
        
        # 列印接收到的資料以調試
        print("Received contest_name:", contest_name)
        print("Received start_date:", start_date)
        print("Received end_date:", end_date)
        print("Received description:", description)
        print("Received type:", description)

        # 確保所有必要的欄位都被正確接收
        if not contest_name or not start_date or not end_date or not description or not type:
            raise ValueError("All contest fields must be provided")

        # 從表單資料中解析題目ID
        contest_data = request.form.to_dict()
        problem_ids = contest_data.get('problem_ids', '').split(',')
        
        if not problem_ids or '' in problem_ids:
            raise ValueError("No problem IDs provided")

        print("Received problem_ids:", problem_ids)

        # 資料庫連線
        connection = db.connection()

        # 新增到contest資料表
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contest (contest_name, start_date, end_date, description, type) VALUES (%s, %s, %s, %s, %s)",
                       (contest_name, start_date, end_date, description, type))
        
        # 取得新建立的contest_id
        contest_id = cursor.lastrowid

        # 循環新增題目到 contest problem 表
        for problem_id in problem_ids:
            connect_contest_and_problem(connection, contest_id, problem_id)

        connection.commit()

        # 比賽建立成功後渲染 create_contest_success.html
        return render_template('create_contest_success.html')
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"status": "error", "message": str(e)})
    finally:
        # 確保關閉資料庫連接
        if connection:
            connection.close()

# 輔助函數：將 contest_id 和 problem_id 關聯起來
def connect_contest_and_problem(connection, contest_id, problem_id):
    cursor = connection.cursor()

    # 插入 contest_id 和 problem_id 到 contest problem 表中
    cursor.execute(
        "INSERT INTO `contest problem` (contest_id, problem_id) VALUES (%s, %s);",
        (contest_id, problem_id)
    )

    cursor.close()

