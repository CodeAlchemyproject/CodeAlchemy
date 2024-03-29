import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pyodbc

def scrape_problem_content_and_save_to_sql_server(problem_id):
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
                problem_content = problem_content_div.text.strip()
                problem_theinput = problem_theinput_div.text.strip()
                problem_theoutput = problem_theoutput_div.text.strip()
                problem_title = span_element.text.strip()
                # 找到所有的 pre 元素
                pre_contents = [pre_element.text.strip() for pre_element in pre_elements]

                # 將範例輸入和範例輸出分別存儲到兩個列表中
                example_inputs = [pre_contents[i] for i in range(0, len(pre_contents), 2)]
                example_outputs = [pre_contents[i + 1] for i in range(0, len(pre_contents), 2)]

                # 將範例輸入和範例輸出合併為同一個變數
                examples_combined_input = '|||'.join(example_inputs)
                examples_combined_output = '|||'.join(example_outputs)

                # 連接到 SQL Server 資料庫
                conn = pyodbc.connect('DRIVER={SQL Server};SERVER=123.192.165.145;DATABASE=CodeAlchemy;UID=sa;PWD=10956CodeAlchemy;CHARSET=UTF8')

                # 創建一個游標對象
                cursor = conn.cursor()

                # 執行 SQL 插入語句
                sql_insert = """
                    INSERT INTO problem (problem_id, title, content, enter_description, output_description, example_input, example_output, difficulty, tag, solved, submission, update_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                # 提供預設值
                default_difficulty = 'N/A'
                default_tag = 'N/A'
                default_solved = 0
                default_submission = 0
                default_update_time = datetime.now()  # 如果不提供值，則預設為 NULL

                # 使用整數值插入
                values = ('ZJ-' + problem_id, problem_title, problem_content, problem_theinput, problem_theoutput, examples_combined_input,
                          examples_combined_output, default_difficulty, default_tag, default_solved, default_submission, default_update_time)

                # 執行 SQL 插入
                cursor.execute(sql_insert, values)

                # 提交事務
                conn.commit()

                # 關閉游標和連接
                cursor.close()
                conn.close()

                print(f'已將題目編號 {problem_id} 的資料儲存到 SQL Server 資料庫中')
            else:
                print('未找到指定的 div 元素')
        except Exception as e:
            print(f'處理題目編號 {problem_id} 時出錯: {str(e)}')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')


# 讀取 CSV 文件中的問題編號
csv_file_path = 'ZJ_problem_list.csv'
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        problem_id = row[0]
        scrape_problem_content_and_save_to_sql_server(problem_id)


print("完成")