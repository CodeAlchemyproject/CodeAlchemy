import requests
from bs4 import BeautifulSoup

# 目標網址
url = "https://zerojudge.tw/Problems?&tabid=BASIC&page=1"

# 發送 GET 請求
response = requests.get(url)

# 解析網頁內容
soup = BeautifulSoup(response.content, "html.parser")

# 使用 XPath 選擇元素
selected_elements = soup.select('div.modal.fade #text')

# 印出選擇到的元素內容
for element in selected_elements:
    print(element.text.strip())
