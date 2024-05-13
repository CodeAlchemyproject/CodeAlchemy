import csv
import random
import time

from crawler import get_problem 

import requests
from bs4 import BeautifulSoup
def TIOJ_get_problem():
    # 目標網址
    url = 'https://tioj.ck.tp.edu.tw/problems/1034'

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查回應狀態碼
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有符合條件的 <div class="panel-body">
        panel_bodies = soup.find_all('div', class_='panel-body')
        
        # 提取第3到第9個 <div class="panel-body"> 的內容
        for i in range(2, 9):  # 注意Python索引從0開始，所以範圍是從2到8
            panel_body = panel_bodies[i]
            print(f"第 {i+1} 個 <div class='panel-body'> 內容：\n{str(panel_body)}\n")
    else:
        print("無法取得網頁內容，狀態碼:", response.status_code)
get_problem.TIOJ_get_problem(1034)
#TIOJ_get_problem()
def get_TIOJ_All_Problem():
    # 讀取 CSV 文件中的問題編號
    csv_file_path = './TIOJ_problem_list.csv'
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            problem_id = row[0]
            get_problem.TIOJ_get_problem(problem_id)
            time.sleep(random.randint(10,20))
