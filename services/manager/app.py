# 匯入必要的模組
import os
import uuid
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import Blueprint
from utils import db

# 產生用戶服務藍圖
manager_bp = Blueprint('manager', __name__)

#--------------------------
# 在user服務藍圖加入路由
#--------------------------
@manager_bp.route('/problem',methods=['GET',"POST"])
def problem():
    if request.method=="POST":
        return render_template()
    else:
        problem_id = request.args.get('problem_id',type=str)
        sql_problem_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_problem_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs)
    