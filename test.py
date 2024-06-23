from datetime import datetime
import random
from utils import db

ensue=['Accepted',
       'Not Accept',
       'Wrong Answer',
       'Time Limit Exceed',
       'Memory Limit Exceed',
       'Output Limit Exceed',
       'Runtime Error',
       'Restricted Function',
       'Compile Error',
       'System Error',
       'Unknown Error']
# 定義對應的權重
weights = [
    60,   # 'Accepted' 的權重
    27,   # 'Not Accept' 的權重
    27,   # 'Wrong Answer' 的權重
    1,    # 'Time Limit Exceed' 的權重
    1,    # 'Memory Limit Exceed' 的權重
    1,    # 'Output Limit Exceed' 的權重
    1,    # 'Runtime Error' 的權重
    1,    # 'Restricted Function' 的權重
    1,    # 'Compile Error' 的權重
    1,    # 'System Error' 的權重
    1     # 'Unknown Error' 的權重
]
language=['python','c++']

user_id=db.get_data('SELECT user_id FROM user;')
user_ids = [user[0] for user in user_id]

problem_id=db.get_data('SELECT problem_id FROM problem where problem_id like "TIOJ%";')
problem_ids= [problem[0] for problem in problem_id]

# 使用random.choices進行隨機選取
for i in range(1,50):   
    e = random.choices(ensue, weights=weights, k=1)[0]
    u = random.choice(user_ids)
    p = random.choice(problem_ids)
    l = random.choice(language)
    r = round(random.uniform(20, 60), 2)
    m = round(random.uniform(15, 40), 2)
    conn = db.connection()
    if conn:
        # 產生執行sql命令的物件, 再執行sql   
        cursor = conn.cursor()
        # 這裡加篩選條件
        sql_command=f'''
            INSERT INTO `answer record` (user_id, problem_id, result, language,run_time,memory, update_time)
            VALUES ('{u}','{p}','{e}', '{l}','{r}','{m}','{str(datetime.now())}')
        '''
        cursor.execute(sql_command)
        conn.commit()


    print(f'user_id: {u}  problem_id: {p}')

# 關閉資料庫連線    
conn.close()
