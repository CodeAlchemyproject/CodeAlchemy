from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 設定 Selenium 的瀏覽器選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 排除無用的日誌訊息
chrome_options.add_argument("disable-infobars")  # 禁用訊息通知

# 自動下載和管理 ChromeDriver
service = Service(ChromeDriverManager().install())

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome(service=service, options=chrome_options)

# try:
#     # 開啟指定的網址
#     driver.get("http://123.192.165.145:8081/Login")

#     # 等待頁面加載，並且等待用戶名和密碼輸入框出現
#     wait = WebDriverWait(driver, 10)  # 最多等待 10 秒

#     # 找到用戶名輸入框，並輸入用戶名
#     username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))  # 假設輸入框的 ID 是 "username"
#     username_field.send_keys("your_username")  # 替換為實際的用戶名

#     # 找到密碼輸入框，並輸入密碼
#     password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))  # 假設輸入框的 ID 是 "password"
#     password_field.send_keys("your_password")  # 替換為實際的密碼

#     # 找到登入按鈕，並點擊
#     login_button = wait.until(EC.presence_of_element_located((By.ID, "loginButton")))  # 假設按鈕的 ID 是 "loginButton"
#     login_button.click()

#     # 等待頁面轉跳或其他後續動作
#     time.sleep(5)  # 你可以修改這段等待的時間

# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     # 結束並關閉瀏覽器
#     driver.quit()
