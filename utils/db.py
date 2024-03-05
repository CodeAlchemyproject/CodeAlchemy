# 匯入連結資料庫模組
import psycopg2

# PostgreSQL連線資訊
DB_HOST = "貼上自己的連線資訊"
DB_NAME = "貼上自己的連線資訊"
DB_USER = "貼上自己的連線資訊"
DB_PASSWORD = "貼上自己的連線資訊"

# 建立資料庫連線
def get_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection