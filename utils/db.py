import pymysql
from pymysql.err import OperationalError

# 定義資料庫連接參數
DB_HOST = '140.131.114.242'
DB_USER = '10956CodeAlchemy'
DB_PASS = 'C0d3@lch3mY_#2024!'
DB_NAME = '113-CodeAlchemy'

def connection():
    try:
        # 建立資料庫連接
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None
      