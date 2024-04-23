# 請將你的程式碼放置於這裡，進行修改和更新
# 需要 import 的模組和套件
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
import traceback

def process_account(username, password, submit_program_dict, language, wait_max=10):
    main_url = 'https://zerojudge.tw/Login'
    language=language
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


        

        # 提交程式
        results = []
        language_upper = language.upper()
        for prob_id, content in submit_program_dict.items():
            results = []
            driver.get(f'https://zerojudge.tw/ShowProblem?problemid={prob_id}')

            btn_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success")))
            btn_code.click()

            btn_py = WebDriverWait(driver, wait_max).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[name='language'][value={language_upper}]")))
            btn_py.click()

            input_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "code")))
            input_code.send_keys(content)

            btn_submit = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "submitCode")))
            btn_submit.click()

            sleep(1)
            table_result = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "table.table-hover")))
            current_row = WebDriverWait(table_result, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))[1]
            sleep(5)
            results.append([])
            for col in WebDriverWait(current_row, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
                results[-1].append(col.text.strip())

            # 將結果存儲到 CSV 文件中
            if results:
                df = pd.DataFrame(results)  # 不包含列名
                # 轉換 DataFrame 為字串
                csv_data = df.to_csv(index=False, header=False, encoding='utf-8')  # 使用UTF-8編碼
                # 寫入 CSV 文件
                with open('result.csv', 'a', encoding='utf-8') as f:  # 使用UTF-8編碼
                    f.write(csv_data)  # 直接寫入CSV數據
                    f.write('\n')  # 添加換行符
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return None

def monitor_source_folder():
    source_folder = './source'
    while True:
        # 監測 source 資料夾是否有新檔案
        files = os.listdir(source_folder)
        if files:
            print("New file detected:", files)
            for file_name in files:
                # 取得檔案的副檔名
                _, extension = os.path.splitext(file_name)
                # 將副檔名轉換為小寫
                extension = extension.lower()
                # 根據副檔名判斷程式語言
                if extension == '.py':
                    language = 'python'
                elif extension == '.java':
                    language = 'java'
                elif extension == '.c':
                    language = 'c'
                elif extension == '.cpp':
                    language = 'cpp'
                else:
                    print(f"Unsupported file format: {extension}")
                    continue

                with open(os.path.join(source_folder, file_name), 'r', encoding='utf-8') as file:
                    content = file.read()
                    submit_program_dict = {os.path.basename(file_name).split('.')[0]: content}

                # 讀取帳戶資訊
                with open('./crawler/account.json', 'r') as file:
                    accounts = json.load(file)['account']
                for acc in accounts:
                    username = acc[0]
                    password = acc[1]
                    results = process_account(username, password, submit_program_dict, language)
                    if results:
                        # 將結果存儲到 CSV 文件中
                        df = pd.DataFrame(results)  # 不包含列名
                        # 轉換 DataFrame 為字串
                        csv_data = df.to_csv(index=False, header=False, encoding='utf-8')  # 使用UTF-8編碼
                        # 寫入 CSV 文件
                        with open('result.csv', 'a', encoding='utf-8') as f:  # 使用UTF-8編碼
                            f.write(csv_data)  # 直接寫入CSV數據
                            f.write('\n')  # 添加換行符

            # 處理完畢後，清空 source 資料夾
            for file in files:
                os.remove(os.path.join(source_folder, file))
        # 暫停一段時間後再次檢查
        sleep(5)

if __name__ == "__main__":
    print("================== start =============")
    # crawler setting
    # 禁用瀏覽器彈窗避免預設路徑載入失敗
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    s = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    #將擴充套件放入至Webdriver的開啟網頁內容
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_extension('./crawler/reCAPTCHA_extension.crx')
    chrome_options.add_extension('./crawler/vpn_extension.crx')
    #隱藏『Chrome正在受到自動軟體的控制』這項資訊
    chrome_options.add_argument("disable-infobars")  

    # 初始化WebDriver
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    wait_max = 10

    # 啟動擴充套件連上VPN
    # 連結套件的html位置
    driver.get("chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html")
    sleep(2)
    # 找到點擊的位置並且點擊
    btn_connect = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "ConnectionButton")))
    btn_connect.click()
    sleep(2)
    # 選擇要切換的視窗根據索引號或視窗標題來選擇
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[0])
    print('crawler setting complete')
    monitor_source_folder()
