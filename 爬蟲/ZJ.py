import requests
from bs4 import BeautifulSoup
import psycopg2

problem_id = input()
print(f'題目編號: {problem_id}')

# 構建完整的 URL
url = f'https://zerojudge.tw/ShowProblem?problemid={problem_id}'

# 發送 GET 請求
response = requests.get(url)

# 檢查是否成功獲取網頁
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到特定的 div 元素
    problem_content_div = soup.find('div', {'id': 'problem_content'})
    problem_theinput_div = soup.find('div', {'id': 'problem_theinput'})
    problem_theoutput_div = soup.find('div', {'id': 'problem_theoutput'})
    pre_elements = soup.find_all('pre')

    # 檢查是否找到
    if problem_content_div and problem_theinput_div and problem_theoutput_div:
        # 獲取內容、輸入說明和輸出說明
        problem_content = problem_content_div.text.strip()
        problem_theinput = problem_theinput_div.text.strip()
        problem_theoutput = problem_theoutput_div.text.strip()

        # 打印出來
        print(f'內容: {problem_content}')
        print(f'輸入說明: {problem_theinput}')
        print(f'輸出說明: {problem_theoutput}')

        # 將找到的值存儲在列表中
        paragraphs = [problem_content]
        enter_description = [problem_theinput]
        output_description = [problem_theoutput]

        # 找到所有的 pre 元素
        pre_contents = [pre_element.text.strip() for pre_element in pre_elements]

        # 逐一印出每個 pre 元素的內容，並區分範例輸入和範例輸出
        for index, pre_content in enumerate(pre_contents, 1):
            tag_name = '範例輸出' if index % 2 == 0 else '範例輸入'
            example_number = (index + 1) // 2  # 調整索引為相同的值
            print(f'{tag_name} {example_number}: {pre_content}')
    else:
        print('未找到指定的 div 元素')
else:
    print(f'網頁請求失敗，狀態碼: {response.status_code}')
