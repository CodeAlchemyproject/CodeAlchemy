import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 設定 Chrome 選項
chrome_options = webdriver.ChromeOptions()

# 使用 WebDriver Manager 自動安裝和管理 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打開 Google 網頁
driver.get('http://www.google.com/')
time.sleep(2)  # 讓用戶看到網頁

# 獲取搜尋框並輸入關鍵字
search_box = driver.find_element("name", "q")  # 使用新的定位方式
search_box.send_keys('ChromeDriver')
search_box.submit()

time.sleep(2)  # 等待搜尋結果顯示
driver.quit()  # 關閉瀏覽器
