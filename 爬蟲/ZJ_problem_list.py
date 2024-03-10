import requests
from bs4 import BeautifulSoup
import csv
import os

# 存放所有問題編號的列表
problem_ids = []

# 32頁的爬蟲
for page in range(1, 33):
    # 構建完整的 URL
    url = f'https://zerojudge.tw/Problems?&tabid=BASIC&page={page}'

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有符合條件的 a 元素
        a_elements = soup.find_all('a', href=lambda href: href and 'ShowProblem?problemid=' in href)

        # 檢查是否找到
        if a_elements:
            # 提取每個<a>元素的href值，並只保留問題編號部分，加入到問題編號列表中
            problem_ids.extend([a_element['href'].split('=')[-1] for a_element in a_elements])
        else:
            print(f'第 {page} 頁未找到指定的<a>元素')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')

# 清除CSV文件內容
csv_file_path = 'ZJ_problem_list.csv'
if os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        pass  # 清空文件內容
else:
    open(csv_file_path, 'w').close()  # 如果文件不存在，則新建一個空文件

# 寫入CSV文件
with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    for problem_id in problem_ids:
        csv_writer.writerow([problem_id])

print('已將問題編號寫入 ZJ_problem_list.csv 文件')
