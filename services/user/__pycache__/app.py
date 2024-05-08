# 匯入Blueprint模組
from flask import request, render_template, jsonify, json,session
from flask import Blueprint


from utils import db

# 產生contest服務藍圖
user_bp = Blueprint('user', __name__)

#--------------------------
# 在contest服務藍圖加入路由
#--------------------------
@user_bp.route('/user_data',methods=['GET'])
def user_data():
    Email = session.get('Email')
    sql_command=f"SELECT * FROM user where email='{Email}'"
    data=db.get_data(sql_command)
    User_id=data[0][0]
    User_name=data[0][1]
    Google_id=data[0][3]
    Email=data[0][4]
    img=data[0][5]
    register_time=data[0][8]
    print(User_id)
    return render_template('./user_data.html',User_id=User_id,User_name=User_name,Google_id=Google_id,Email=Email,img=img,register_time=register_time)