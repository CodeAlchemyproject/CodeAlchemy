# 引入所需的模組和套件
from queue import Queue
from flask import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from time import sleep
import os
import glob

# crawler setting
main_url = 'https://zerojudge.tw/Login'
# 禁用瀏覽器彈窗避免預設路徑載入失敗
prefs = {'profile.default_content_setting_values':{'notifications': 2}}
language='python'
s = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
#將擴充套件放入至Webdriver的開啟網頁內容
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_extension('./crawler/reCAPTCHA_extension.crx')
chrome_options.add_extension('./crawler/vpn_extension.crx')
#隱藏『Chrome正在受到自動軟體的控制』這項資訊
chrome_options.add_argument("disable-infobars")  
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()
wait_max = 10

#啟動擴充套件連上VPN
#連結套件的html位置
driver.get("chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html")
sleep(2)
#找到點擊的位置並且點擊
btn_connect = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "ConnectionButton")))
btn_connect.click()
sleep(2)
# 選擇要切換的視窗根據索引號或視窗標題來選擇
all_windows = driver.window_handles
driver.switch_to.window(all_windows[0])
# 讀取所有檔案
submit_program_dict = dict()
py_files = glob.glob(f'./source/*.*')
for file_name in py_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content)
        submit_program_dict[os.path.basename(file_name).split('.')[0]] = content
        print(submit_program_dict[os.path.basename(file_name).split('.')[0]])
# 讀取帳戶資訊
with open('./crawler/account.json', 'r') as file: 
    accounts = json.load(file)['account']
for acc in accounts:
    username = acc[0]
    print(username)
    password = acc[1]
    print(password)
    # 構建資料夾的路徑
    folder_path = os.path.join('./source')
    # 檢查該資料夾是否存在並且是否為空
    if not os.path.exists(folder_path) and os.listdir(folder_path):
        continue
    
    # 登錄網站
    driver.get(main_url)
    try:
        login_area = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-md-4.text-center')))
        login_area = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-horizontal')))

        sleep(2)

        input_username = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'account')))
        input_username.send_keys(username)

        sleep(2)

        input_password = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'passwd')))
        input_password.send_keys(password)
        
        sleep(3)
        
        for i in range(60):
            sleep(1)
            try:
                btn_login = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-primary')))
                btn_login.click()
                break
            except: pass
        else: raise BaseException
        
        sleep(5)
        
        if driver.current_url != 'https://zerojudge.tw/': raise BaseException

    except BaseException as e:
        print(e)
    
    # 提交程式
    results = []
    language_upper = language.upper()
    for prob_id in list(submit_program_dict.keys()):
        print()
        results = []
        driver.get(f'https://zerojudge.tw/ShowProblem?problemid={prob_id}')

        btn_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success")))
        btn_code.click()
        
        btn_py = WebDriverWait(driver, wait_max).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[name='language'][value='{language_upper}']")))

        btn_py.click()
        
        input_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "code")))
        input_code.send_keys(submit_program_dict[prob_id])
        
        btn_submit = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "submitCode")))
        btn_submit.click()

        sleep(1)
        table_result = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "table.table-hover")))
        current_row = WebDriverWait(table_result, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))[1]
        
        results.append([])
        for col in WebDriverWait(current_row, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
            results[-1].append(col.text.strip())

    # 將結果存儲到 CSV 文件中
    if results:
        df = pd.DataFrame(results)  # 不包含列名
        # 轉換 DataFrame 為字串
        csv_data = df.to_csv(index=False, header=False)  # 不寫入列名
        print(csv_data)
        csv_data = csv_data.encode('big5').decode('utf-8')
        # 寫入 CSV 文件
        with open('result.csv', 'a') as f:
            f.write(csv_data.rstrip('\r\n') + '\n')  # 添加換行符

# # 刪除source資料夾下的所有檔案
# folder_path = './source'
# for file_name in os.listdir(folder_path):
#     file_path = os.path.join(folder_path, file_name)
#     os.remove(file_path)
# driver.quit()