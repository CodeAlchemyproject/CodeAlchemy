import mysql.connector as connector

# 建立資料庫連線
connection = connector.connect(
        user="root", password="12345", host="127.0.0.1", database="sakila"
    )
      