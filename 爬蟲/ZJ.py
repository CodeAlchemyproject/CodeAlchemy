import requests
from bs4 import BeautifulSoup

# 讓使用者輸入problemid
problem_id = input('請輸入problemid: ')

# 構建完整的URL
url = f'https://zerojudge.tw/ShowProblem?problemid={problem_id}'

# 發送GET請求
response = requests.get(url)

# 檢查是否成功獲取網頁
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到特定的span元素
    problem_title_span = soup.find('span', {'id': 'problem_title'})

    # 檢查是否找到
    if problem_title_span:
        # 獲取標題文字
        problem_title = problem_title_span.text.strip()
        print(f'題目標題: {problem_title}')
    else:
        print('未找到指定的span元素')

    # 找到所有的p元素
    p_elements = soup.find_all('p')

    # 檢查是否找到
    if p_elements:
        # 逐一印出每個p元素的內容
        for index, p_element in enumerate(p_elements, 1):
            print(f'段落 {index}: {p_element.text.strip()}')
    else:
        print('未找到任何p元素')

    # 找到所有的pre元素
    pre_elements = soup.find_all('pre')

    # 檢查是否找到
    if pre_elements:
        # 逐一印出每個pre元素的內容
        for index, pre_element in enumerate(pre_elements, 1):
            print(f'Pre {index}: {pre_element.text.strip()}')
    else:
        print('未找到任何pre元素')
else:
    print(f'網頁請求失敗，狀態碼: {response.status_code}')
