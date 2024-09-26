# 匯入Blueprint模組
from flask import request, render_template, jsonify, json, redirect, session
import sqlite3
from flask import Blueprint
from flask_login import current_user


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
@contest_bp.route('/join/form')
def contest_join():    
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    # **使用者 ID，假設已經有登入系統並且 session 中有 user_id
    user_id = session['User_id']
    
    # 從請求中取得頁碼，預設為第一頁
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每頁顯示的比賽數量

    offset = (page - 1) * per_page  # 計算目前頁的起始位置

    total_contests_query = "SELECT COUNT(*) FROM contest"
    cursor.execute(total_contests_query)
    total_contests = cursor.fetchone()[0]  # 取得總比賽數

    # 修改這個查詢以包含適當的ORDER BY子句，以確保資料是按照開始時間的降序傳回的
    query = """
    SELECT contest_id, contest_name, start_date, end_date, description, type 
    FROM contest 
    ORDER BY contest_id DESC  -- 这里假设你希望根据start_date字段排序
    LIMIT %s OFFSET %s
    """
    
    cursor.execute(query, (per_page, offset))
    contests = cursor.fetchall()

    # **查詢該用戶參加過的比賽
    cursor.execute("SELECT contest_id FROM `contest participant` WHERE user_id = %s", (user_id,))
    joined_contests = set([row[0] for row in cursor.fetchall()])  # 得到參加過的比賽 ID 集合
    
    conn.close()

    # **添加參加狀態到 contests 中
    contests_with_status = []
    for contest in contests:
        contest_id = contest[0]
        if contest_id in joined_contests:
            contests_with_status.append((*contest, "joined"))
        else:
            contests_with_status.append((*contest, "not_joined"))

    total_pages = (total_contests + per_page - 1) // per_page  # 計算總頁數
    
    return render_template('join_contest_form.html', contests=contests, page=page, total_pages=total_pages)
'''


@contest_bp.route('/join/form')
def contest_join():    
    conn = db.connection()  # Get database connection
    cursor = conn.cursor()

    # 使用者 ID，假設已經有登入系統並且 session 中有 user_id
    user_id = session['User_id']
    
    # 從請求中取得頁碼，預設為第一頁
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每頁顯示的比賽數量

    offset = (page - 1) * per_page  # 計算目前頁的起始位置

    # 獲取總比賽數
    total_contests_query = "SELECT COUNT(*) FROM contest"
    cursor.execute(total_contests_query)
    total_contests = cursor.fetchone()[0]

    # 查詢比賽資料
    query = """
    SELECT contest_id, contest_name, start_date, end_date, description, type 
    FROM contest 
    ORDER BY contest_id DESC
    LIMIT %s OFFSET %s
    """
    
    cursor.execute(query, (per_page, offset))
    contests = cursor.fetchall()

    # 查詢該用戶參加過的比賽
    cursor.execute("SELECT contest_id FROM `contest participant` WHERE user_id = %s", (user_id,))
    joined_contests = set([row[0] for row in cursor.fetchall()])  # 取得該使用者參加過的比賽 ID

    conn.close()

    # 添加參加狀態到 contests 中
    contests_with_status = []
    for contest in contests:
        contest_id = contest[0]
        if contest_id in joined_contests:
            contests_with_status.append((*contest, "joined"))
        else:
            contests_with_status.append((*contest, "not_joined"))

    total_pages = (total_contests + per_page - 1) // per_page
    
    return render_template('join_contest_form.html', contests=contests_with_status, page=page, total_pages=total_pages)



'''OK
@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form.get('contest_id')
    #user_id = request.form.get('user_id')  # **假设用户ID以某种方式（如表单或会话）传递

    #**
    #if not contest_id or not user_id:
        #flash('Missing contest ID or user ID.', 'error')
        #return redirect(url_for('display_page'))  # 修改为适当的重定向

    conn = db.connection()
    cursor = conn.cursor()

    # **检查该用户是否已加入比赛
    #cursor.execute("SELECT * FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    #if cursor.fetchone():
        #flash('You have already joined this contest.', 'info')
        #conn.close()
        #return redirect(url_for('display_page'))  # 修改为适当的重定向    

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

    # 加入比赛
    #cursor.execute("INSERT INTO `contest participant` (contest_id, user_id) VALUES (%s, %s)", (contest_id, user_id)) #**
    #conn.commit() #**
    conn.close()

    #flash('You have successfully joined the contest.', 'success')
    #return redirect(url_for('display_page'))  # 修改为适当的重定向
  
    # 將查詢結果傳遞給模板
    return render_template('contest_joined.html', contest_name=contest_name, start_time=start_time, end_time=end_time, problems=problems)
'''



@contest_bp.route('/join', methods=['POST'])
def join_contest():
    contest_id = request.form['contest_id']
    # 假設你已經在使用者登入時取得了使用者的 user_id
    user_id = session['User_id']
    
    conn = db.connection()
    cursor = conn.cursor()

    # 檢查該使用者是否已經參加過該比賽
    cursor.execute("SELECT 1 FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    already_joined = cursor.fetchone()

    # 如果尚未參加過該比賽，則寫入 contest participant 資料表
    if not already_joined:
        cursor.execute("INSERT INTO `contest participant` (contest_id, user_id) VALUES (%s, %s)", (contest_id, user_id))
        conn.commit()

    # 查詢比賽名稱、開始時間和結束時間
    cursor.execute("SELECT contest_name, start_date, end_date FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return "比赛不存在", 404  # 如果查不到數據，回傳錯誤訊息

    contest_name = result[0]
    start_time = result[1]
    end_time = result[2]

    # 查詢與該比賽相關的所有主題 problem_id, title, difficulty
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

