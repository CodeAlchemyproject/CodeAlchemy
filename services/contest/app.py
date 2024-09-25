# 匯入Blueprint模組
from flask import request, render_template, jsonify, json, redirect, url_for, flash
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

'''(contest list無頁碼版)
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


@contest_bp.route('/join/form')
def contest_join():
    contest_id = request.form['contest_id']#**
    user_id = request.form['user_id']  # **这里假定前端表单中有包含user_id的信息，或者从session中获取当前登录用户的user_id
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    # **检查用户是否已经加入了该比赛
    cursor.execute("SELECT * FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    if cursor.fetchone():
        # 如果已经加入，可以选择返回一个提示消息
        conn.close()
        flash('You have already joined this contest.', 'info')  # 使用 flash 提示用户
        return redirect(url_for('your_contest_list_page'))  # 返回比赛列表页面或其他适当的页面

    # 从请求中获取页码，默认为第一页
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示的比赛数量

    offset = (page - 1) * per_page  # 计算当前页的起始位置

    total_contests_query = "SELECT COUNT(*) FROM contest"
    cursor.execute(total_contests_query)
    total_contests = cursor.fetchone()[0]  # 获取总比赛数

    # 修改这个查询以包含适当的ORDER BY子句，以确保数据是按照开始时间的降序返回的
    query = """
    SELECT contest_id, contest_name, start_date, end_date, description, type 
    FROM contest 
    ORDER BY contest_id DESC  -- 这里假设你希望根据start_date字段排序
    LIMIT %s OFFSET %s
    """
    
    cursor.execute(query, (per_page, offset))
    contests = cursor.fetchall()

    # **向 contest participant 表中插入记录
    cursor.execute("INSERT INTO `contest participant` (contest_id, user_id) VALUES (%s, %s)", (contest_id, user_id))
    conn.commit()#**
    conn.close()

    total_pages = (total_contests + per_page - 1) // per_page  # 计算总页数

    flash('You have successfully joined the contest.', 'success')  # **提示用户成功加入比赛
    # 渲染 join_contest.html，传入 contests 和分页信息
    return render_template('join_contest_form.html', contests=contests, page=page, total_pages=total_pages)


'''
@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    conn = db.connection()
    cursor = conn.cursor()

    # 查詢比賽名稱、開始時間和結束時間
    cursor.execute("SELECT contest_name, start_date, end_date FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return "比賽不存在", 404  # 如果查不到資料，返回錯誤訊息

    contest_name = result[0]
    start_time = result[1]
    end_time = result[2]

    # 將查詢結果傳遞給模板
    return render_template('contest_joined.html', contest_name=contest_name, start_time=start_time, end_time=end_time)
'''

'''
@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    conn = db.connection()
    cursor = conn.cursor()

    # 查詢比賽名稱、開始時間和結束時間
    cursor.execute("SELECT contest_name, start_date, end_date FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return "比賽不存在", 404  # 如果查不到資料，返回錯誤訊息

    contest_name = result[0]
    start_time = result[1]
    end_time = result[2]

    # 查詢與該比賽相關的所有題目 problem_id
    cursor.execute("SELECT problem_id FROM `contest problem` WHERE contest_id = %s", (contest_id,))
    problems = cursor.fetchall()

    conn.close()
  
    # 將查詢結果傳遞給模板
    return render_template('contest_joined.html', contest_name=contest_name, start_time=start_time, end_time=end_time, problems=problems)
'''


@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    conn = db.connection()
    cursor = conn.cursor()

    # 查詢比賽名稱、開始時間和結束時間
    cursor.execute("SELECT contest_name, start_date, end_date FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return "比賽不存在", 404  # 如果查不到資料，返回錯誤訊息

    contest_name = result[0]
    start_time = result[1]
    end_time = result[2]

    # 查詢與該比賽相關的所有題目 problem_id, title, difficulty
    cursor.execute("""
        SELECT p.problem_id, p.title, p.difficulty
        FROM `contest problem` cp 
        JOIN `problem` p ON cp.problem_id = p.problem_id 
        WHERE cp.contest_id = %s
    """, (contest_id,))
    problems = cursor.fetchall()

    conn.close()
  
    # 將查詢結果傳遞給模板
    return render_template('contest_joined.html', contest_name=contest_name, start_time=start_time, end_time=end_time, problems=problems)







@contest_bp.route('/get_problems')
def get_problems():
    # 取得URL參數中的page和per_page變量，如果沒有則分別預設為1和10
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # 建立到資料庫的連接
    conn = db.connection()
    cur = conn.cursor()
    
    # 計算應該跳過的記錄數
    offset = (page - 1) * per_page
    # 执行分页查询
    cur.execute("SELECT problem_id, title, content, difficulty FROM problem LIMIT %s OFFSET %s;", (per_page, offset))
    problems_data = cur.fetchall()
    
    # 取得資料庫中題目的總數以計算頁數
    cur.execute("SELECT COUNT(*) FROM problem;")
    total_problems = cur.fetchone()[0]
    total_pages = (total_problems + per_page - 1) // per_page  # 計算總分頁數
    
    # 關閉連接
    cur.close()
    conn.close()
  
    # 返回查詢結果給前端，附加分頁信息
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

