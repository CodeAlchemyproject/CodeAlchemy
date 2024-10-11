# 匯入Blueprint模組
from flask import request, render_template, jsonify, json, redirect, session, url_for
import sqlite3
from flask import Blueprint
from datetime import datetime


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
    # 檢查使用者是否已登入
    user_id = session.get('User_id')
    if not user_id:
        # 如果未登入，渲染 login.html 並顯示提示訊息
        #flash('請先登入以參加比賽', 'warning')  # 可以顯示提示訊息
        return render_template('login.html')  # 直接渲染登入頁面
    return render_template('create_contest.html') 


'''
@contest_bp.route('/join/form')
def contest_join():
    conn = db.connection()  # 獲取資料庫連接
    cursor = conn.cursor()

    current_time = datetime.now()  # 獲取當前時間

    # 檢查使用者 ID 是否存在於 session 中
    user_id = session.get('User_id')

    # 獲取 URL 中的篩選條件
    state = request.args.get('state', None)  # 獲取比賽狀態參數，默認為 None
    page = request.args.get('page', 1, type=int)  # 獲取頁碼，默認為第 1 頁
    per_page = 10  # 每頁顯示的比賽數量
    offset = (page - 1) * per_page  # 計算目前頁的起始位置

    # 獲取總比賽數的查詢條件
    total_contests_query = "SELECT COUNT(*) FROM contest"

    # 用來篩選比賽狀態和類型的條件
    where_clause = []
    params = []  # 存放參數

    if state == 'public':
        where_clause.append("type = 'public'")
    elif state == 'private':
        where_clause.append("type = 'private'")
    elif state == 'not_started':
        where_clause.append("start_date > %s")
        params.append(current_time)  # 將 current_time 加入參數
    elif state == 'ongoing':
        where_clause.append("start_date <= %s AND end_date > %s")
        params.extend([current_time, current_time])  # 兩次使用 current_time
    elif state == 'finished':
        where_clause.append("end_date <= %s")
        params.append(current_time)  # 將 current_time 加入參數


    # 構建完整的 SQL 查詢
    if where_clause:
        total_contests_query += " WHERE " + " AND ".join(where_clause)

    # 執行查詢，計算比賽數量
    cursor.execute(total_contests_query, tuple(params))  # 只在有參數時傳入
    total_contests = cursor.fetchone()[0]

    # 查詢比賽資料的查詢條件
    contest_query = """
    SELECT contest_id, contest_name, start_date, end_date, description, type
    FROM contest
    """

    # 添加篩選條件
    if where_clause:
        contest_query += " WHERE " + " AND ".join(where_clause)

    # 排序及分頁
    contest_query += " ORDER BY contest_id DESC LIMIT %s OFFSET %s"

    # 執行查詢比賽資料
    cursor.execute(contest_query, tuple(params + [per_page, offset]))
    contests = cursor.fetchall()


    # 查詢每個比賽的參加人數
    contest_participants_query = """
    SELECT contest_id, COUNT(user_id) 
    FROM `contest participant` 
    GROUP BY contest_id
    """
    cursor.execute(contest_participants_query)
    contest_participants = cursor.fetchall()

    # 將比賽ID對應到參加人數
    contest_participants_dict = {row[0]: row[1] for row in contest_participants}

    # 添加參加狀態到 contests 中
    contests_with_status = []
    for contest in contests:
        contest_id = contest[0]
        participant_count = contest_participants_dict.get(contest_id, 0)

        # 使用從資料庫讀取的 start_date 和 end_date，這已經是 datetime 物件
        start_date = contest[2]  # 假設這是 datetime 物件
        end_date = contest[3]    # 假設這是 datetime 物件
        
        # 計算剩餘天數
        remaining_days = (end_date - current_time).days
        remaining_seconds = (end_date - current_time).seconds  # 剩餘的秒數

        if start_date > current_time:  # 比賽尚未開始
            countdown_days = (start_date - current_time).days
            countdown_hours = (start_date - current_time).seconds // 3600
            if countdown_days >= 1:
                time_status = f"倒數 {countdown_days} 天開始"
            elif countdown_days < 1:
                if countdown_hours >= 1:
                    time_status = f"倒數 {countdown_hours} 小時開始"
                else:
                    time_status = "即將開始"
        elif remaining_days > 0 or (remaining_days == 0 and remaining_seconds > 0):  # 比賽進行中
            if remaining_days == 0:  # 剩餘小於一天
                remaining_hours = (end_date - current_time).seconds // 3600  # 計算剩餘小時數
                time_status = f"比賽將在 {remaining_hours} 小時後結束"
            else:
                time_status = f"剩餘天數: {remaining_days} 天"
        else:  # 比賽已結束
            time_status = "比賽已結束"

        if user_id:
            cursor.execute("SELECT contest_id FROM `contest participant` WHERE user_id = %s", (user_id,))
            joined_contests = set([row[0] for row in cursor.fetchall()])
            status = "joined" if contest_id in joined_contests else "not_joined"
        else:
            status = "not_joined"

        contests_with_status.append((*contest, status, participant_count, time_status))

    # 檢查是否有比賽資料並添加相應的訊息
    no_contest_message = None
    if not contests:
        if state == 'ongoing':
            no_contest_message = "沒有正在進行中的比賽"
        elif state == 'not_started':
            no_contest_message = "沒有尚未開始的比賽"
        elif state == 'contest_type':
            no_contest_message = "沒有符合條件的比賽"

    total_pages = (total_contests + per_page - 1) // per_page

    conn.close()

    return render_template('join_contest_form.html', contests=contests_with_status, 
                           page=page, total_pages=total_pages, 
                           current_time=current_time, 
                           no_contest_message=no_contest_message)
'''

@contest_bp.route('/join/form')
def contest_join():
    conn = db.connection()
    cursor = conn.cursor()

    current_time = datetime.now()
    user_id = session.get('User_id')

    # 獲取 URL 中的篩選條件
    state = request.args.get('state', None)
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # 獲取總比賽數的查詢條件
    total_contests_query = "SELECT COUNT(*) FROM contest"
    where_clause = []
    params = []

    # 添加狀態過濾條件
    if state == 'public':
        where_clause.append("type = 'public'")
    elif state == 'private':
        where_clause.append("type = 'private'")
    elif state == 'not_started':
        where_clause.append("start_date > %s")
        params.append(current_time)
    elif state == 'ongoing':
        where_clause.append("start_date <= %s AND end_date > %s")
        params.extend([current_time, current_time])
    elif state == 'finished':
        where_clause.append("end_date <= %s")
        params.append(current_time)

    # 添加搜尋條件
    if search:
        where_clause.append("contest_name LIKE %s")
        params.append(f"%{search}%")

    # 構建完整的 SQL 查詢
    if where_clause:
        total_contests_query += " WHERE " + " AND ".join(where_clause)

    cursor.execute(total_contests_query, tuple(params))
    total_contests = cursor.fetchone()[0]

    # 查詢比賽資料
    contest_query = """
    SELECT contest_id, contest_name, start_date, end_date, description, type
    FROM contest
    """
    if where_clause:
        contest_query += " WHERE " + " AND ".join(where_clause)
    contest_query += " ORDER BY contest_id DESC LIMIT %s OFFSET %s"
    cursor.execute(contest_query, tuple(params + [per_page, offset]))
    contests = cursor.fetchall()

    # 查詢每個比賽的參加人數
    contest_participants_query = """
    SELECT contest_id, COUNT(user_id) 
    FROM `contest participant` 
    GROUP BY contest_id
    """
    cursor.execute(contest_participants_query)
    contest_participants = cursor.fetchall()

    # 將比賽ID對應到參加人數
    contest_participants_dict = {row[0]: row[1] for row in contest_participants}

    # 添加參加狀態到 contests 中
    contests_with_status = []
    for contest in contests:
        contest_id = contest[0]
        participant_count = contest_participants_dict.get(contest_id, 0)

        start_date = contest[2]
        end_date = contest[3]

        remaining_days = (end_date - current_time).days
        remaining_seconds = (end_date - current_time).seconds

        if start_date > current_time:
            countdown_days = (start_date - current_time).days
            countdown_hours = (start_date - current_time).seconds // 3600
            if countdown_days >= 1:
                time_status = f"倒數 {countdown_days} 天開始"
            elif countdown_days < 1:
                if countdown_hours >= 1:
                    time_status = f"倒數 {countdown_hours} 小時開始"
                else:
                    time_status = "即將開始"
        elif remaining_days > 0 or (remaining_days == 0 and remaining_seconds > 0):
            if remaining_days == 0:
                remaining_hours = (end_date - current_time).seconds // 3600
                time_status = f"比賽將在 {remaining_hours} 小時後結束"
            else:
                time_status = f"剩餘天數: {remaining_days} 天"
        else:
            time_status = "比賽已結束"

        if user_id:
            cursor.execute("SELECT contest_id FROM `contest participant` WHERE user_id = %s", (user_id,))
            joined_contests = set([row[0] for row in cursor.fetchall()])
            status = "joined" if contest_id in joined_contests else "not_joined"
        else:
            status = "not_joined"

        contests_with_status.append((*contest, status, participant_count, time_status))

    no_contest_message = None
    if not contests:
        if state == 'ongoing':
            no_contest_message = "沒有正在進行中的比賽"
        elif state == 'not_started':
            no_contest_message = "沒有尚未開始的比賽"
        elif state == 'contest_type':
            no_contest_message = "沒有符合條件的比賽"

    total_pages = (total_contests + per_page - 1) // per_page

    conn.close()

    return render_template('join_contest_form.html', contests=contests_with_status, 
                           page=page, total_pages=total_pages, 
                           state=state, search=search, current_time=current_time, 
                           no_contest_message=no_contest_message)





@contest_bp.route('/join', methods=["POST"])
def join_contest():
    contest_id = request.form['contest_id']
    input_password = request.form.get('contest_password')

    # 請確保 session 中正確設定了使用者ID
    user_id = session.get('User_id')
    
    if not user_id:
        # 用戶未登錄，返回狀態碼和訊息
        return jsonify({"error": "请先登录", "code": "not_logged_in"}), 403
    
    conn = db.connection()
    cursor = conn.cursor()

    cursor.execute("SELECT type, password FROM contest WHERE contest_id = %s", (contest_id,))
    contest = cursor.fetchone()
    
    if not contest:
        conn.close()
        return jsonify({"error": "比賽不存在"}), 404
    
    contest_type, contest_password = contest

    if contest_type == 'private':
        if not input_password or input_password != contest_password:
            return jsonify({"error": "比賽密碼錯誤"}), 403

    cursor.execute("SELECT 1 FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    already_joined = cursor.fetchone()

    if not already_joined:
        cursor.execute("INSERT INTO `contest participant` (contest_id, user_id) VALUES (%s, %s)", (contest_id, user_id))
        conn.commit()

    conn.close()

    return jsonify({"redirect_url": url_for('contest_bp.contest_info', contest_id=contest_id)})


'''##no private password run##
@contest_bp.route('/join', methods=["POST"])
def join_contest():
    contest_id = request.form['contest_id']
    
    # 檢查使用者 ID 是否存在於 session 中
    user_id = session.get('User_id')
    
    # 如果使用者未登入，渲染 login.html
    if not user_id:
        return render_template('./login.html')

    conn = db.connection()
    cursor = conn.cursor()

    # 檢查該使用者是否已經參加過該比賽
    cursor.execute("SELECT 1 FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    already_joined = cursor.fetchone()

    # 如果尚未參加過該比賽，則寫入 contest participant 資料表
    if not already_joined:
        cursor.execute("INSERT INTO `contest participant` (contest_id, user_id) VALUES (%s, %s)", (contest_id, user_id))
        conn.commit()

    conn.close()
    
    # 使用 redirect 重導向到顯示結果的 GET 路由
    return redirect(url_for('contest_bp.contest_info', contest_id=contest_id))
'''

@contest_bp.route('/contest/<contest_id>', methods=["GET"])
def contest_info(contest_id):
    user_id = session['User_id']
    
    conn = db.connection()
    cursor = conn.cursor()

    # 檢查該使用者是否有參加該比賽
    cursor.execute("SELECT 1 FROM `contest participant` WHERE contest_id = %s AND user_id = %s", (contest_id, user_id))
    joined = cursor.fetchone()

    if not joined:
        conn.close()
        return "你未參加該比賽，無法查看相關資訊", 403  # 如果使用者未參加該比賽，返回 403 錯誤

    # 查詢比賽名稱、開始時間和結束時間
    cursor.execute("SELECT contest_name, start_date, end_date FROM contest WHERE contest_id = %s", (contest_id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return "比賽不存在", 404  # 如果查不到數據，回傳錯誤訊息

    contest_name = result[0]
    start_time = result[1]
    end_time = result[2]

    # 查詢與該比賽相關的所有題目及是否完成
    cursor.execute(""" 
        SELECT p.problem_id, p.title, p.difficulty,
               CASE 
                   WHEN EXISTS (SELECT 1 FROM `contest submission` cs 
                                WHERE cs.problem_id = p.problem_id AND cs.contest_id = %s 
                                AND cs.user_id = %s AND cs.is_finish = 'Accepted') 
                   THEN 1 
                   ELSE 0 
               END AS is_finished
        FROM `contest problem` cp 
        JOIN `problem` p ON cp.problem_id = p.problem_id 
        WHERE cp.contest_id = %s
    """, (contest_id, user_id, contest_id))
    problems = cursor.fetchall()

    # Contest Rank 查詢
    data = db.get_data(f'''
        SELECT 
            cs.contest_id,
            u.user_name,
            u.image,
            SUM(CASE WHEN cs.is_finish = 'Accepted' THEN 1 ELSE 0 END) AS 正確答題數,
            CONCAT(ROUND(SUM(CASE WHEN cs.is_finish = 'Accepted' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2), '%') AS 答題正確率,
            ROUND(AVG(cs.run_time), 2) AS 平均執行時間,
            ROUND(AVG(cs.memory), 2) AS 平均使用記憶體
        FROM `113-CodeAlchemy`.`contest submission` cs
        JOIN `113-CodeAlchemy`.`user` u ON cs.user_id = u.user_id
        WHERE cs.contest_id = {contest_id}  -- 直接將 contest_id 嵌入查詢語句中
        GROUP BY cs.contest_id, u.user_name, u.image
        ORDER BY 正確答題數 DESC, 答題正確率 DESC, 平均執行時間, 平均使用記憶體;
    ''')

    conn.close()

    # 傳遞 contest_id 和 data 給模板
    return render_template('contest_joined.html', contest_name=contest_name, start_time=start_time, end_time=end_time, problems=problems, contest_id=contest_id, data=data)



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
        contest_type = request.form.get('state')  # 修改此行來獲取下拉選單的值
        contest_password = None  # 預設密碼為None

        # 如果比賽類型為私人，則獲取密碼
        if contest_type == "private":
            contest_password = request.form.get('contest_password')
            if not contest_password:
                raise ValueError("私人比賽必須設定密碼")
        
        # 列印接收到的資料以調試
        print("Received contest_name:", contest_name)
        print("Received start_date:", start_date)
        print("Received end_date:", end_date)
        print("Received description:", description)
        print("Received type:", contest_type)  # 修改此行以匹配 contest_type

        # 確保所有必要的欄位都被正確接收
        if not contest_name or not start_date or not end_date or not description or not contest_type:
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
        cursor.execute("INSERT INTO contest (contest_name, start_date, end_date, description, type, password) VALUES (%s, %s, %s, %s, %s, %s)",
                       (contest_name, start_date, end_date, description, contest_type, contest_password))
        
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

