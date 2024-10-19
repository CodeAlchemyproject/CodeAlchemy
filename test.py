# from crawler.submit import CodeAlchemy_submit
# CodeAlchemy_submit('da2b80_CA-a001.py','17','CAOJ-a001')
from utils import db

problem_id='CAOJ-1001'
title=db.get_data(f'''SELECT title FROM `113-CodeAlchemy`.problem where problem_id ='{problem_id}';''')[0]
print(title)