import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_problem_content_and_print(problem_id):
    # 构建完整的 URL
    url = f'https://zerojudge.tw/ShowProblem?problemid={problem_id}'

    # 发送 GET 请求
    response = requests.get(url)

    # 检查是否成功获取网页
    if response.status_code == 200:
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到特定的 div 元素
            problem_content_div = soup.find('div', {'id': 'problem_content'})
            span_element = soup.find('span', {'id': 'problem_title'})
            span_statistics = soup.find('span', title='解題統計')

            # 检查是否找到
            if span_element and problem_content_div:
                # 获取标题和内容
                problem_title = span_element.text.strip()
                problem_content = problem_content_div.text.strip()

                # 获取输入和输出
                input_output_divs = soup.find_all('div', {'id': ['problem_theinput', 'problem_theoutput']})
                input_output_texts = [div.text.strip() for div in input_output_divs]

                # 获取标签
                tag_div = soup.find('div', class_='problem_tag')
                tag = tag_div.text.strip() if tag_div else 'N/A'

                # 获取解题统计百分比
                statistics_percentage = 'N/A'
                if span_statistics:
                    statistics_text = span_statistics.text.strip()
                    last_10_chars = statistics_text[-10:]
                    statistics_percentage = ''.join(filter(str.isdigit, last_10_chars))

                    # 根据百分比确定难度等级
                    if statistics_percentage:
                        percentage_value = int(statistics_percentage)
                        if percentage_value >= 80:
                            difficulty = 'easy'
                        elif percentage_value >= 60:
                            difficulty = 'normal'
                        else:
                            difficulty = 'hard'
                    else:
                        difficulty = 'N/A'
                else:
                    difficulty = 'N/A'

                # 打印问题信息
                print(f'Problem Title: {problem_title}')
                print(f'Problem Content: {problem_content}')
                print(f'Problem Input: {input_output_texts[0]}')
                print(f'Problem Output: {input_output_texts[1]}')
                print(f'Tag: {tag}')
                print(f'Difficulty: {difficulty}')
                print(f'Statistics Percentage: {statistics_percentage}')

            else:
                print('未找到指定的元素')
        except Exception as e:
            print(f'处理问题 {problem_id} 时出错: {str(e)}')
    else:
        print(f'网页请求失败，状态码: {response.status_code}')
scrape_problem_content_and_print("a001")