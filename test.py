import json
import os
import threading

from utils import common
from 爬蟲.ZJ_submit import process_account

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

# 假設有三個目標文件夾
target_folders = ['./爬蟲/src/BeAPro113', './爬蟲/src/TestCase2024', './爬蟲/src/yyyiii']

# 將文件分配到目標文件夾中
common.distribute_files('./source', target_folders)

# 讀取帳戶資訊
with open('./爬蟲/account.json', 'r') as file: 
    accounts = json.load(file)['account']

# 多執行序
threads = []
for acc in accounts:
    username = acc[0]
    password = acc[1]
    #執行提交程序
    thread = threading.Thread(target=process_account, args=(username, password, language))
    threads.append(thread)
    thread.start()
    
for thread in threads:
    thread.join()