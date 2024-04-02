import pyodbc

# 建立資料庫連線
def get_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=123.192.165.145;DATABASE=CodeAlchemy;UID=sa;PWD=10956CodeAlchemy;CHARSET=UTF8')
     
    return conn