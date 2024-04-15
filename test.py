import json
import os
import threading

from utils import common
from crawler.ZJ_submit import process_account

problem_id = 'a001'
language = 'python'
content = '''print(f'hello, {input()}')'''

# 定義語言對應的文件擴展名字典
file_extensions = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp'
}

# 構建文件路徑
file_path = os.path.join('./source', f'{problem_id}{file_extensions[language]}')

# 確保目錄存在
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# 寫入內容到文件中
with open(file_path, 'w') as file:
    file.write(content)

# 假設有兩個目標文件夾
target_folders = ['./crawler/src/TestCase2024','./crawler/src/BeAPro113', './crawler/src/yyyiii']

# 將文件分配到目標文件夾中
common.distribute_files('./source', target_folders)

# 讀取帳戶資訊
with open('./crawler/account.json', 'r') as file: 
    accounts = json.load(file)['account']

# 多執行序
threads = []
for acc in accounts:
    username = acc[0]
    password = acc[1]
    # 構建該使用者資料夾的路徑
    user_folder_path = os.path.join('./crawler/src/', username)
    # 檢查該資料夾是否存在並且是否為空
    if os.path.exists(user_folder_path) and os.listdir(user_folder_path):
        # 如果該資料夾存在並且不為空，則進行處理
        # 將該使用者資料夾下的檔案加入執行序中
        for file_name in os.listdir(user_folder_path):
            file_path = os.path.join(user_folder_path, file_name)
            if os.path.isfile(file_path):
                thread = threading.Thread(target=process_account, args=(username, password, language))
                threads.append(thread)
                thread.start()
    else:
        # 如果該資料夾不存在或者為空，則顯示相應的訊息
        print(f"資料夾 {username} 為空，未加入執行序。")

# 等待所有執行序完成
for thread in threads:
    thread.join()
