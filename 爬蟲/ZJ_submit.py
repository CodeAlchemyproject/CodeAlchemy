import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
# 設置浏覽器驅動程序的路徑
driver_path = "C:\\Users\\My_User\\Documents\\msedgedriver.exe"

# 初始化 WebDriver
options = webdriver.EdgeOptions()
options.binary_location = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'


# 創建 WebDriver
driver = webdriver.Edge(options=options)

# 將 Cookies 加載到瀏覽器中
# 從文件中讀取 Cookies
with open("ZJ-login.txt", "r") as file:
    cookies_data = file.read()
# 解析 JSON 字符串
try:
    cookies = json.loads(cookies_data)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON data from file.")
    cookies = []
for cookie in cookies:
    # 确保 cookie 是一个字典对象
    if isinstance(cookie, dict):
        driver.add_cookie(cookie)
    else:
        print(f"Error: Invalid cookie format - {cookie}")

# 打開網頁
driver.get("https://zerojudge.tw/ShowProblem?problemid=a001")

# 在這裡添加你的網頁操作，如點擊、填寫表單等
time.sleep(50)
# 關閉瀏覽器
driver.quit()