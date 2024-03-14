import requests

# 登入所需的帳號和密碼
login_data = {
    'account': 'chouenyu940808@gmail.com',
    'passwd': ''
}

# 登入頁面的 URL
login_url = 'https://zerojudge.tw/Login'

# 創建一個 Session 對象
session = requests.Session()

# 發送登入請求
response = session.post(login_url, data=login_data)

# 檢查是否登入成功
if 'Welcome' in response.text:
    print("登入成功！")
    # 在此處可以繼續爬取其他頁面的操作
    # 例如：
    # response = session.get('https://zerojudge.tw/SomeOtherPage')
    # 然後處理 response 的內容
else:
    print("登入失敗！")
