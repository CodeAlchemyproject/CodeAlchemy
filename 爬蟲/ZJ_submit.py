from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設置浏覽器驅動程序的路徑
driver_path = "C:\\Users\\My_User\\Documents\\msedgedriver.exe"

# 創建一個 Edge WebDriver 對象
options = webdriver.EdgeOptions()
options.binary_location = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
driver = webdriver.Edge(options=options, executable_path=driver_path)

# 設置要搜索的關鍵詞
search_query = "ZeroJudge"

# 打開 Google 網頁
driver.get("https://zerojudge.tw/ShowProblem?problemid=a001")

# 使用顯性等待，等待輸入框可見並且可交互
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "account"))
)

# 輸入搜索關鍵詞，然後按 Enter 鍵
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 停留一段時間，觀察搜索結果
input("觀察搜索結果後按 Enter 鍵關閉瀏覽器...")

# 關閉瀏覽器
driver.quit()
