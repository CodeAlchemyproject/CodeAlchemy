import csv
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils import db

def ZJ_get_problem(problem_id):
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
                problem_title = span_element.text.split()
                if type(problem_title)==list:
                    problem_title = ' '.join(problem_title)
                # 使用正規表達式將第一個<p>前面的所有文字和最後一個</p>後面的文字去除
                problem_content = re.sub(r'^.*?<p>', '<p>', problem_content, 1)
                problem_content = re.sub(r'</p>.*?$', '</p>', problem_content, 1)
                problem_content = problem_content[:-6]
                problem_theinput = re.sub(r'^.*?<p>', '<p>', problem_theinput, 1)
                problem_theinput = re.sub(r'</p>.*?$', '</p>', problem_theinput, 1)
                problem_theoutput = re.sub(r'^.*?<p>', '<p>', problem_theoutput, 1)
                problem_theoutput = re.sub(r'</p>.*?$', '</p>', problem_theoutput, 1)
                
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

                # 連接到 My SQL 資料庫
                conn=db.connection()

                # 創建一個游標對象
                cursor = conn.cursor()

                # 執行 SQL 插入語句
                sql_insert = """
                    INSERT INTO problem (problem_id, title, content, enter_description, output_description, `example input`, `example output`, difficulty, tag, solved, submission, update_time, collection)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """


                # 提供預設值
                default_difficulty = difficulty
                default_tag = tag
                default_solved = 0
                default_submission = 0
                default_update_time = datetime.now()  # 如果不提供值，則預設為 NULL
                default_collection=0

                # 使用整數值插入
                values = ('ZJ-' + problem_id, problem_title, problem_content, problem_theinput, problem_theoutput, examples_combined_input,
                          examples_combined_output, default_difficulty, default_tag, default_solved, default_submission, default_update_time,default_collection)

                # 執行 SQL 插入
                cursor.execute(sql_insert, values)

                # 提交事務
                conn.commit()

                print(f'已將題目編號 {problem_id} 的資料儲存到 My SQL 資料庫中')
            else:
                print('未找到指定的 div 元素')
        except Exception as e:
            print(f'處理題目編號 {problem_id} 時出錯: {str(e)}')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')
    response.close()

def ZJ_get_problem_list():
    # 存放所有問題編號的列表
    problem_ids = []
    problem_type={'BASIC':32,'CONTEST':23,'TOI':29,'UVA':29,'ORIGINAL':47}
    for problem_category, end_page in problem_type.items():
        for page in range(1,end_page+1):
            url=f'https://zerojudge.tw/Problems?&tabid={problem_category}&page={page}'
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
    with open('ZJ_problem_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for problem_id in problem_ids:
            csv_writer.writerow([problem_id])

    print('已將問題編號寫入 ZJ_problem_list.csv 文件')

def TIOJ_get_problem(problem_id):
    # 構建完整的 URL
    problem_id=str(problem_id)
    url = f'https://tioj.ck.tp.edu.tw/problems/{problem_id}'
    # 發送 GET 請求
    response = requests.get(url)

    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到所有符合條件的 <div class="panel-body">
            panel_bodies = soup.find_all('div', class_='panel-body')

            if len(panel_bodies) >= 7:
                # problem_id 題目編號
                problem_id = "TIOJ" +'-'+ problem_id
                
                # title 標題
                problem_title = soup.find('h4', class_='page-header').get_text().split('.')[1].strip()
                
                # [2]難度等級percentage
                AC_Ratio = panel_bodies[2].text.strip()
                percentage = AC_Ratio.split()[0][:2]
                # 根据百分比确定难度等级
                if percentage:
                    percentage_value = int(percentage)
                    if percentage_value >= 60:
                        difficulty = 'easy'
                    elif percentage_value >= 40:
                        difficulty = 'normal'
                    else:
                        difficulty = 'hard'
                else:
                    difficulty = 'N/A'


                # [3]標籤Tag
                target_panel_body = panel_bodies[3]
                # 找到其中的所有 <a> 標籤
                a_tags = target_panel_body.find_all('a')
                if a_tags:
                    # 如果存在 <a> 標籤，取出其文本並以逗號隔開
                    tag = ", ".join([a.get_text() for a in a_tags])
                else:
                    # 如果不存在 <a> 標籤，設置為 "N/A"
                    tag = "N/A"
                    
                # [4] 敘述 Description
                                                    # 去掉<div class="panel-body">
                                                    # 去掉</div>
                problem_content = str(panel_bodies[4]).replace('<div class="panel-body">', '').replace('<div class="panel-body">', '')

                # [5][6] 輸出輸入說明
                problem_theinput = str(panel_bodies[5]).replace('<div class="panel-body">', '').replace('<div class="panel-body">', '')
                problem_theoutput = str(panel_bodies[6]).replace('<div class="panel-body">', '').replace('<div class="panel-body">', '')
                
                # [7][8] 輸入輸出範例

                examples = soup.find_all('div', class_='panel-body code-input copy-group-code')

                print(examples)
                print("\n")

                # # 連接到 My SQL 資料庫
                # conn=db.connection()

                # # 創建一個游標對象
                # cursor = conn.cursor()

                # # 執行 SQL 插入語句
                # sql_insert = """
                #     INSERT INTO problem (problem_id, title, content, enter_description, output_description, `example input`, `example output`, difficulty, tag, solved, submission, update_time, collection)
                #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                # """


                # # 提供預設值
                # default_difficulty = difficulty
                # default_tag = tag
                # default_solved = 0
                # default_submission = 0
                # default_update_time = datetime.now()  # 如果不提供值，則預設為 NULL
                # default_collection=0

                # # 使用整數值插入
                # values = (problem_id, problem_title, problem_content, problem_theinput, problem_theoutput, examples_input,
                #             examples_output, default_difficulty, default_tag, default_solved, default_submission, default_update_time,default_collection)

                # # 執行 SQL 插入
                # cursor.execute(sql_insert, values)

                # # 提交事務
                # conn.commit()

                print(f'已將題目編號 {problem_id} 的資料儲存到 My SQL 資料庫中')
            else:
                print('未找到指定的 div 元素')
        except Exception as e:
            print(f'處理題目編號 {problem_id} 時出錯: {str(e)}')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')

def TIOJ_get_problem_list():
    # 存放所有問題編號的列表
    problem_ids = []
    # 爬取指定範圍的頁面
    end_page=17
    url_pattern='https://tioj.ck.tp.edu.tw/problems?page='
    for page in range(1, end_page + 1):
        # 構建完整的 URL
        url = f'{url_pattern}{page}'
        # 發送GET請求
        response = requests.get(url)

        # 檢查回應狀態碼，200表示成功
        if response.status_code == 200:
            # 解析HTML內容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 找到目標表格
            table = soup.find('table', class_='table table-hover table-striped')
            
            if table:
                # 找到tbody
                tbody = table.find('tbody')
                
                if tbody:
                    # 找到所有的tr
                    trs = tbody.find_all('tr')
                    
                    # 迴圈處理每一個tr，取得第二個td的文字
                    for tr in trs:
                        # 找到第二個td
                        second_td = tr.find_all('td')[1]  # 因為Python從0開始計數，所以第二個td的索引是1
                        
                        if second_td:
                            # 取得文字內容
                            text = second_td.get_text(strip=True)
                            problem_ids.append(text)
                        else:
                            print("找不到第二個td")
                else:
                    print("找不到tbody")
            else:
                print("找不到目標表格")
        else:
            print("無法取得網頁內容，狀態碼:", response.status_code)
        
        # 寫入 CSV 文件
    with open('TIOJ_problem_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for problem_id in problem_ids:
            csv_writer.writerow([problem_id])

    print('已將問題編號寫入 TIOJ_problem_list.csv 文件')