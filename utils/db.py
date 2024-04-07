import pymysql
from pymysql.err import OperationalError

# 定義資料庫連接參數
DB_HOST = '140.131.114.242'
DB_USER = '10956CodeAlchemy'
DB_PASS = 'C0d3@lch3mY_#2024!'
DB_NAME = '113-CodeAlchemy'

# 建立資料庫連接
def connection():
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None
    
# 取得並篩選資料
def get_data(sql_command):
    # 取得資料庫連線 
    conn = connection()
    if conn:
        try:
            # 產生執行sql命令的物件, 再執行sql   
            cursor = conn.cursor()
            # 這裡加篩選條件
            cursor.execute(sql_command)
            # 取出資料
            data = cursor.fetchall()
            return data
        finally:
            # 關閉資料庫連線    
            conn.close()
    else:
        return None

# 新增、更新、刪除資料
def edit_data(sql_command):
    # 取得資料庫連線 
    conn = connection()
    if conn:
        try:
            # 產生執行sql命令的物件, 再執行sql   
            cursor = conn.cursor()
            # 這裡加篩選條件
            cursor.execute(sql_command)
            conn.commit()
        finally:
            # 關閉資料庫連線    
            conn.close()
    else:
        print("Failed to establish database connection.")