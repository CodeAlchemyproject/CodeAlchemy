import requests
from bs4 import BeautifulSoup
import csv
import psycopg2

def scrape_problem_content_and_save_to_postgres(problem_id):

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

           # 找到所有的 pre 元素
            pre_contents = [pre_element.text.strip() for pre_element in pre_elements]

            # 將範例輸入和範例輸出分別存儲到兩個列表中
            example_inputs = [pre_contents[i] for i in range(0, len(pre_contents), 2)]
            example_outputs = [pre_contents[i+1] for i in range(0, len(pre_contents), 2)]

            # 將範例輸入和範例輸出合併為同一個變數
            examples_combined_input = '|||'.join(example_inputs)
            examples_combined_output = '|||'.join(example_outputs)

            # 打印範例輸入和範例輸出
            print(f'範例輸入: {examples_combined_input}')
            print(f'範例輸出: {examples_combined_output}')

            # 連接到 PostgreSQL 資料庫
            conn = psycopg2.connect(
                host="satao.db.elephantsql.com",
                database="你的資料庫名稱",
                user="你的使用者名稱",
                password="你的密碼"
            )

            # 創建一個遊標對象
            cursor = conn.cursor()

            # 執行 SQL 插入語句
            sql_insert = """
                INSERT INTO problems (problem_id, title, content, enter_description, output_description, example_input, example_output)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # 使用整數值插入
            values = (problem_id, title, problem_content, problem_theinput, problem_theoutput, examples_combined)

            # 執行 SQL 插入
            cursor.execute(sql_insert, values)


            # 提交事務
            conn.commit()

            # 關閉遊標和連接
            cursor.close()
            conn.close()

            print(f'已將題目編號 {problem_id} 的資料儲存到 PostgreSQL 資料庫中')
        else:
            print('未找到指定的 div 元素')
    else:
        print(f'網頁請求失敗，狀態碼: {response.status_code}')

# 讀取 CSV 文件中的問題編號
csv_file_path = 'ZJ_problem_list.csv'
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # 跳過標題行
    for row in csv_reader:
        problem_id = row[0]
        scrape_problem_content_and_save_to_postgres(problem_id)