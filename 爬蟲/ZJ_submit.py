from datetime import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 設定瀏覽器驅動程式的路徑，這裡以Chrome為例
driver_path = 'C:\\Users\\My_User\\Documents\\chromedriver_win64\\chromedriver_win64\\chromedriver.exe'

# 創建一個Chrome服務對象
service = Service(driver_path)

# 創建一個Chrome WebDriver對象，並指定服務
driver = webdriver.Chrome(service=service)

# 目標URL
url = 'https://zerojudge.tw/Login'
driver.get(url)

# 找到帳號和密碼的input元素，並輸入資料
account_input = driver.find_element_by_id('account')
account_input.send_keys('codealchemyproject@gmail.com')

passwd_input = driver.find_element_by_id('passwd')
passwd_input.send_keys('10956CodeAlchemy')

# 等待一段時間，確保reCAPTCHA載入完畢
time.sleep(5)

# 如果reCAPTCHA是由iframe包含的，需要先切換到iframe
# driver.switch_to.frame('reCAPTCHA iframe id')

# 點擊提交按鈕
submit_button = driver.find_element_by_xpath('//button[@type="submit"]')
submit_button.click()

# 等待一段時間，觀察登入結果或後續操作
time.sleep(5)

# 關閉瀏覽器
driver.quit()
