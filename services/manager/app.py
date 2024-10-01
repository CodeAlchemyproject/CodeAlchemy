# 匯入必要的模組
from flask import request, render_template, redirect, session
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
    try:
        if session['Permission']=='Manager':
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
                tag=data.get('tag')
                video_id=data.get('video_id')
                sql_command=f"INSERT INTO `113-CodeAlchemy`.`problem` (`problem_id`, `title`, `content`, `enter_description`, `output_description`, `example_input`, `example_output`, `difficulty`, `tag`, `video_id` ,`solved`, `submission`, `update_time`) VALUES ('CAOJ-{new_no}', '{title}', '{content}', '{enter_description}', '{output_description}', '{example_input}' , '{example_output}', '{difficulty}', '{tag}', '{video_id}', '0', '0', '{datetime.now()}');"
                db.edit_data(sql_command)
                return redirect('/')
            else:
                return render_template('./add_problem.html')
    except:
        return redirect('/')
@manager_bp.route('/problem',methods=['GET',"POST"])
def problem():
    try:
        if session['Permission']=='Manager':
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
                tag=data.get('tag')
                video_id=data.get('video_id')
                sql_problem_command=f"UPDATE problem SET title = '{title}',content = '{content}',enter_description = '{enter_description}',output_description = '{output_description}',example_input = '{example_input}',example_output = '{example_output}' ,difficulty='{difficulty}' ,tag='{tag}' ,video_id='{video_id}' WHERE problem_id = '{problem_id}';"
                db.edit_data(sql_problem_command)
                sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
                problem_data=db.get_data(sql_command)
                example_inputs = problem_data[0][5].split('|||')
                example_outputs = problem_data[0][6].split('|||')
                tag = problem_data[0][8]
                video_id = problem_data[0][9]
                return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,difficulty=difficulty,tag=tag,video_id=video_id)
            else:
                problem_id = request.args.get('problem_id',type=str)
                sql_command=f"SELECT * FROM problem where problem_id='{problem_id}'"
                problem_data=db.get_data(sql_command)
                example_inputs = problem_data[0][5].split('|||')
                example_outputs = problem_data[0][6].split('|||')
                difficulty = problem_data[0][7]
                tag= problem_data[0][8]
                video_id = problem_data[0][9]
                return render_template('./manager_problem.html',data=problem_data,example_inputs=example_inputs,example_outputs=example_outputs,difficulty=difficulty,tag=tag,video_id=video_id)
    except:
        return redirect('/')
@manager_bp.route('/user', methods=['GET','POST'])
def user():
    try:
        if session["Permission"]=='Manager':
            if request.method=='GET':
                sql_command=f"SELECT * FROM `113-CodeAlchemy`.user;"
                user_data=db.get_data(sql_command)
                return render_template('./manager_user.html',data=user_data )
            else:
                new_data=request.form
                new_data=list(new_data.items())
                sql_command=f"SELECT * FROM `113-CodeAlchemy`.user;"
                user_data=db.get_data(sql_command)
                for i in range(len(new_data)):
                    if new_data[i][1]!=user_data[i][6]:
                        sql_command=f"UPDATE `113-CodeAlchemy`.`user` SET `permission` = '{new_data[i][1]}' WHERE (`user_id` = '{user_data[i][0]}');"
                        db.edit_data(sql_command)
                sql_command=f"SELECT * FROM `113-CodeAlchemy`.user;"
                user_data=db.get_data(sql_command)
                return render_template('./manager_user.html',data=user_data)
    except:
        return redirect('/')
@manager_bp.route('/delete',methods=['GET'])
def delete():
    try:
        if session["Permission"]=='Manager':
            problem_id = request.args.get('problem_id',type=str)
            sql_command=f"DELETE FROM problem where problem_id='{problem_id}'"
            db.edit_data(sql_command)
            return redirect('/')
    except:
        return redirect('/')