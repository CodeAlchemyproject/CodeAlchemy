# 匯入必要的模組
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import Blueprint
from utils import db

from datetime import datetime

# 產生用戶服務藍圖
manager_bp = Blueprint('manager', __name__)

#--------------------------
# 在user服務藍圖加入路由
#--------------------------
@manager_bp.route('add_problem',methods=["GET","POST"])
def add_problem():
    if request.method=="POST":
        #給新題號
        sql_command="SELECT * FROM `113-CodeAlchemy`.problem where problem_id like 'CAOJ%' order by problem_id desc;"
        old_no=db.get_data(sql_command)[0][0].split('-')[1]
        new_no=int(old_no)+1
        #處理新增題目內容
        data=request.form
        title=data.get('title')
        content=data.get('content')
        enter_description=data.get('enter_description')
        output_description=data.get('output_description')
        example_input=data.get('example_input')
        example_output=data.get('example_output')
        difficulty=data.get('difficulty')
        print(title)
        sql_command=f"INSERT INTO `113-CodeAlchemy`.`problem` (`problem_id`, `title`, `content`, `enter_description`, `output_description`, `example_input`, `example_output`, `difficulty`, `tag`, `solved`, `submission`, `update_time`) VALUES ('CAOJ-{new_no}', '{title}', '{content}', '{enter_description}', '{output_description}', '{example_input}' , '{example_output}', '{difficulty}', 'N/A', '0', '0', '{datetime.now()}');"
        db.edit_data(sql_command)
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
        difficulty=data.get('difficulty')
        sql_problem_command=f"UPDATE problem SET title = '{title}',content = '{content}',enter_description = '{enter_description}',output_description = '{output_description}',example_input = '{example_input}',example_output = '{example_output}' ,difficulty='{difficulty}' WHERE problem_id = '{problem_id}';"
        db.edit_data(sql_problem_command)
        sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        like = db.get_data(f"SELECT IFNULL(COUNT(*),0) FROM collection where problem_id='{problem_id}'")[0][0]
        return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,difficulty=difficulty)
    else:
        problem_id = request.args.get('problem_id',type=str)
        sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
        problem_data=db.get_data(sql_command)
        example_inputs = problem_data[0][5].split('|||')
        example_outputs = problem_data[0][6].split('|||')
        difficulty = problem_data[0][7]
        return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,difficulty=difficulty)
    
@manager_bp.route('/delete',methods=['GET'])
def delete():
    problem_id = request.args.get('problem_id',type=str)
    sql_command=f"DELETE FROM problem where problem_id='{problem_id}'"
    db.edit_data(sql_command)
    return redirect('/')