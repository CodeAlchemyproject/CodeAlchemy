import os
from utils import db
from config import gemini_api_key
# 單個純文字
import json
import requests
# user_id = session['User_id']
def clean_string(s: str) -> str:
    # 找到 "text": 的位置
    text_start_index = s.find('"text":')
    if text_start_index != -1:
        # 截取 "text": 之後的部分
        s = s[text_start_index + len('"text":'):]

    # 找到 "role": 的位置
    role_start_index = s.find('"role":')
    if role_start_index != -1:
        # 截取 "role": 之前的部分
        s = s[:role_start_index]

    # 去掉最後三個字
    if len(s) > 3:
        s = s[:-3]

    return s.strip()  # 去掉首尾空白字元

def find_best_code(problem_id,user_id):
    MyBestRecord=db.get_data(f'''SELECT record_id, run_time, memory, update_time
    FROM `answer record`
    WHERE user_id = {int(user_id)} AND problem_id = '{problem_id}'AND run_time!=0 AND memory!=0
    ORDER BY run_time ASC, memory ASC, update_time ASC
    LIMIT 1;
    ''')
    AllBestRecord=db.get_data(f'''SELECT record_id, run_time, memory, update_time
    FROM `answer record`
    WHERE user_id != {int(user_id)} AND problem_id = '{problem_id}'AND run_time!=0 AND memory!=0
    ORDER BY run_time ASC, memory ASC, update_time ASC
    LIMIT 1;
    ''')
   

    # 根據最佳紀錄找到檔案路徑
    def find_best_record_file(record_id, problem_id):
        filename = f"{record_id}_{problem_id}.py"
        filepath = os.path.join("source", "accept", filename)
        return filepath

    # 查詢當前使用者的最佳紀錄
    current_user_best_record = MyBestRecord

    # 查詢其他使用者的最佳紀錄
    all_users_best_record = AllBestRecord

    # 假設查詢結果的結構是 (record_id, run_time, memory, update_time)
    current_user_best_record = MyBestRecord[0] if MyBestRecord else None
    all_users_best_record = AllBestRecord[0] if AllBestRecord else None
    if int(MyBestRecord[0][1])>int(AllBestRecord[0][1]):
        pre='A效能>B'
    else:
        pre='B效能>A'
    if current_user_best_record and all_users_best_record and current_user_best_record[0] == all_users_best_record[0]:
        print("當前使用者的最佳提交已是所有使用者的最佳提交，無需進一步比較。")
        return False
    else:
        current_user_filepath = find_best_record_file(current_user_best_record[0], problem_id)
        all_users_filepath = find_best_record_file(all_users_best_record[0], problem_id)

        return [current_user_filepath,all_users_filepath,pre]
    
# 讀取檔案內容
def read_file_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    else:
        print(f"檔案 {filepath} 不存在。")
        return None
def gemini_api_analyse(file_list):
    api_key=gemini_api_key
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}'
    headers = {'Content-Type': 'application/json'}
    a_code=read_file_content(file_list[0])
    b_code=read_file_content(file_list[1])
    text=f"對比A程式碼{a_code}和B程式碼{b_code} 的資料結構使用，並分析為何{file_list[2]}，要能淺顯易懂。"
    data = {
        "contents": [
            {
                "parts": [{"text":text}]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"response status_code: {response.status_code}")
    response_data=json.dumps(response.json(), indent=4, ensure_ascii=False)
    response_data=clean_string(response_data)
    return(response_data)
