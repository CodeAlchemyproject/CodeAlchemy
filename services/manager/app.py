# 匯入必要的模組
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import Blueprint
from utils import db

# 產生用戶服務藍圖
manager_bp = Blueprint('manager', __name__)

#--------------------------
# 在user服務藍圖加入路由
#--------------------------
@manager_bp.route('add_problem',methods=["GET","POST"])
def add_problem():
    if request.method=="POST":
        sql_command=""
        return redirect('/')
    else:
        return render_template('./add_problem.html')
@manager_bp.route('/problem',methods=['GET',"POST"])
def problem():
    if request.method=="POST":
        data=request.form
        problem_id=data.get('problem_id')
        title=data.get('title')
        content=data.get('content')
        enter_description=data.get('enter_description')
        output_description=data.get('output_description')
        example_input=data.get('example_input')
        example_output=data.get('example_output')
        sql_problem_command=f"UPDATE problem SET title = '{title}',content = '{content}',enter_description = '{enter_description}',output_description = '{output_description}',example_input = '{example_input}',example_output = '{example_output}' WHERE problem_id = '{problem_id}';"
        db.edit_data(sql_problem_command)
        sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        like = db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}'")[0][0]
        return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,like=like)
    else:
        problem_id = request.args.get('problem_id',type=str)
        sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        like = db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}'")[0][0]
        return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,like=like)
    
@manager_bp.route('/delete',methods=['GET'])
def delete():
    problem_id = request.args.get('problem_id',type=str)
    sql_command=f"DELETE FROM problem where problem_id='{problem_id}'"
    db.edit_data(sql_command)
    return redirect('/')