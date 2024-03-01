from bs4 import BeautifulSoup
import requests
def test():
    # 構建完整的 URL
    problem_id=str(problem_id)
    url = f'http://192.168.2.100/problem?problem_id=ZJ-a001'
    # 發送 GET 請求
    response = requests.get(url)

    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(response.text, 'html5lib')
            GAWA = soup.find_all('p')
            print(GAWA.get_text().strip())

        except Exception as e:
            print(f'出錯: {str(e)}').
            0.0