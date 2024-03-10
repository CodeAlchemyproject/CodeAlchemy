import requests
from bs4 import BeautifulSoup

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

# 一次性打印所有問題編號
print('所有問題編號:', problem_ids)
