import random
import re
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

def scrape_problem_content(problem_id):
    # 構建完整的 URL
    url = f'https://zerojudge.tw/ShowProblem?problemid={problem_id}'

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到特定的 div 元素
            problem_content_div = soup.find('div', {'id': 'problem_content'})
            problem_theinput_div = soup.find('div', {'id': 'problem_theinput'})
            problem_theoutput_div = soup.find('div', {'id': 'problem_theoutput'})
            pre_elements = soup.find_all('pre')
            span_element = soup.find('span', {'id': 'problem_title'})
            # 檢查是否找到
            if span_element and problem_content_div and problem_theinput_div and problem_theoutput_div:
                # 獲取內容、輸入說明和輸出說明
                problem_content = str(problem_content_div)
                problem_theinput = str(problem_theinput_div)
                problem_theoutput = str(problem_theoutput_div)
                problem_title = str(span_element)
                # 找到所有的 pre 元素
                pre_contents = [str(pre_element) for pre_element in pre_elements]

                # 將範例輸入和範例輸出分別存儲到兩個列表中
                example_inputs = [pre_contents[i] for i in range(0, len(pre_contents), 2)]
                example_outputs = [pre_contents[i + 1] for i in range(0, len(pre_contents), 2)]

                # 將範例輸入和範例輸出合併為同一個變數
                examples_combined_input = '|||'.join(example_inputs)
                examples_combined_output = '|||'.join(example_outputs)
                # 获取标签
                tag_div = soup.find('span', class_='tag')
                tag = tag_div.text.strip() if tag_div else 'N/A'

                # 假設soup是BeautifulSoup的一個實例，已經找到了對應的元素
                string = soup.find('span', title='解題統計').text.strip()
                

                # 使用正規表達式將非數字部分去除，並將剩下的數字放在清單中
                numbers_only = re.findall(r'\d+', string)  # 找到所有的數字
                numbers = [int(num) for num in numbers_only]  # 將字符串轉換為整數
                percentage=numbers[-1]
                    


                # 根据百分比确定难度等级
                if percentage:
                    percentage_value = int(percentage)
                    if percentage_value >= 80:
                        difficulty = 'easy'
                    elif percentage_value >= 60:
                        difficulty = 'normal'
                    else:
                        difficulty = 'hard'
                else:
                    difficulty = 'N/A'

                print(f"題目標題: {problem_title}")
                print(f"題目內容: {problem_content}")
                print(f"輸入說明: {problem_theinput}")
                print(f"輸出說明: {problem_theoutput}")
                print(f"範例輸入: {examples_combined_input}")
                print(f"範例輸出: {examples_combined_output}")
                print(f"標籤: {tag}")
                print(f"難度等級: {difficulty}")

                response.close()
            else:
                print('未找到指定的 div 元素')
        except Exception as e:
            print(f'處理題目編號 {problem_id} 時出錯: {str(e)}')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')

scrape_problem_content('b924')
