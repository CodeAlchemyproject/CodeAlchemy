import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_problem_ids(url_pattern, start_page, end_page, csv_file_path):
    # 存放所有問題編號的列表
    problem_ids = []

    # 爬取指定範圍的頁面
    for page in range(start_page, end_page + 1):
        # 構建完整的 URL
        url = f'{url_pattern}{page}'

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

    # 寫入 CSV 文件
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for problem_id in problem_ids:
            csv_writer.writerow([problem_id])

    print(f'已將問題編號寫入 {csv_file_path} 文件')

# 爬取 BASIC 分類的問題
scrape_problem_ids('https://zerojudge.tw/Problems?&tabid=BASIC&page=', 1, 32, 'ZJ_problem_list.csv')

# 爬取 CONTEST 分類的問題
scrape_problem_ids('https://zerojudge.tw/Problems?&tabid=CONTEST&page=', 1, 23, 'ZJ_problem_list.csv')

# 爬取 TOI 分類的問題
scrape_problem_ids('https://zerojudge.tw/Problems?&tabid=TOI&page=', 1, 29, 'ZJ_problem_list.csv')

# 爬取 UVA 分類的問題
scrape_problem_ids('https://zerojudge.tw/Problems?&tabid=UVA&page=', 1, 29, 'ZJ_problem_list.csv')

# 爬取 ORIGINAL 分類的問題
scrape_problem_ids('https://zerojudge.tw/Problems?&tabid=ORIGINAL&page=', 1, 47, 'ZJ_problem_list.csv')
