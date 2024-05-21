# 引入所需的模組和套件
from datetime import datetime
from flask import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from time import sleep
import os
import glob
import traceback

def TIOJ_submit(file_name, number):
    main_url = 'https://tioj.ck.tp.edu.tw/users/sign_in'
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None
    results = []  # 初始化 results 變數

    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_extension('./crawler/extension/reCAPTCHA_extension.crx')
        chrome_options.add_extension('./crawler/extension/vpn_extension.crx')
        chrome_options.add_argument("disable-infobars")

        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.maximize_window()
        wait_max = 10

        driver.get("chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html")
        sleep(2)
        btn_connect = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "ConnectionButton")))
        btn_connect.click()
        sleep(2)
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[0])

        submit_program_dict = dict()
        files = glob.glob(f'./source/{file_name}')
        
        for file_name in files:
            _, extension = os.path.splitext(file_name)
            extension = extension.lower()
           
            if extension == '.py':
                language = 'python'
            elif extension == '.java':
                language = 'java'
            elif extension == '.c':
                language = 'c'
            elif extension == '.cpp':
                language = 'cpp'

            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                file_key = os.path.basename(file_name)[7:].replace("TIOJ-", "").split('.')[0]
                submit_program_dict[file_key] = content

        with open('./crawler/account.json', 'r') as file:
            accounts = json.load(file)['account']
        for acc in accounts:
            if acc[0][0-len(number):]==number:
                username = acc[0]
                password = acc[1]
                driver.get(main_url)
                try:
                    input_username = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.NAME, 'user[username]')))
                    input_username.send_keys(username)
                    sleep(1)

                    input_password = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.NAME, 'user[password]')))
                    input_password.send_keys(password)
                    sleep(1)

                    sign_in = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.NAME, 'commit')))
                    sign_in.click()
                    sleep(1)

                    if driver.current_url != 'https://tioj.ck.tp.edu.tw/':
                        raise BaseException
                
                except BaseException as e:
                    print(e)
                    continue
                
                language_dict = {
                    "python": "9",
                    "cpp": "12"
                }
                value = language_dict.get(language)
                for prob_id in list(submit_program_dict.keys()):
                    driver.get(f'https://tioj.ck.tp.edu.tw/problems/{prob_id}/submissions/new')
                    compiler = Select(WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "submission_compiler_id"))))
                    compiler.select_by_value(value)
                    sleep(1)

                    input_code = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "submission_code_content_attributes_code")))
                    input_code.send_keys(submit_program_dict[prob_id])
                    sleep(1)

                    btn_submit = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "form-submit-button")))
                    btn_submit.click()
                    sleep(1)

                    result = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "verdict")))
                    results.append(result.text)

                    run_time = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "td-time-0")))
                    results.append(run_time.text)

                    memory = WebDriverWait(driver, wait_max).until(
                        EC.presence_of_element_located((By.ID, "td-vss-0")))
                
                    results.append(round(int(memory.text)/1024,2))
                    sleep(1)

        if results:
            df = pd.DataFrame([results])
            csv_data = df.to_csv(index=False, header=False, encoding='utf-8')
            with open('./crawler/result.csv', 'a', encoding='utf-8') as f:
                f.write(number + ",")
                f.write(file_key + ",")
                f.write(csv_data.strip() + ",")
                f.write(language)
                f.write(str(datetime.now()))  # 轉換為字符串
                f.write('\n')

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        print(results)
        return results

def ZeroJudge_Submit(file_name,number):
    # crawler setting
    main_url = 'https://zerojudge.tw/Login'
    # 禁用瀏覽器彈窗避免預設路徑載入失敗
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None  # 初始化 driver 變數
    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        # 將擴充套件放入至Webdriver的開啟網頁內容
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_extension('./crawler/extension/reCAPTCHA_extension.crx')
        chrome_options.add_extension('./crawler/extension/vpn_extension.crx')
        # 隱藏『Chrome正在受到自動軟體的控制』這項資訊
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

        # 讀取所有檔案
        submit_program_dict = dict()
        files = glob.glob(f'./source/{file_name}')
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
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                # 提取檔案名稱中除去前六位的部分作為 key
                file_key = os.path.basename(file_name)[7:].replace("ZJ-", "").split('.')[0]
                print(file_key)
                submit_program_dict = {file_key: content}
        # 讀取帳戶資訊
        with open('./crawler/account.json', 'r') as file:
            accounts = json.load(file)['account']
        for acc in accounts:
            if number==acc[0].split('-')[0]:
                username = acc[0]
                password = acc[1]

            # 登錄網站
            driver.get(main_url)
            try:
                login_area = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, 'col-md-4.text-center')))
                login_area = WebDriverWait(login_area, wait_max).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'form-horizontal')))

                sleep(2)

                input_username = WebDriverWait(login_area, wait_max).until(
                    EC.presence_of_element_located((By.ID, 'account')))
                input_username.send_keys(username)

                sleep(2)

                input_password = WebDriverWait(login_area, wait_max).until(
                    EC.presence_of_element_located((By.ID, 'passwd')))
                input_password.send_keys(password)

                sleep(3)

                for i in range(300):
                    sleep(1)
                    try:
                        btn_login = WebDriverWait(login_area, wait_max).until(
                            EC.presence_of_element_located((By.type, 'btn.btn-primary')))
                        btn_login.click()
                        break
                    except:
                        pass
                else:
                    raise BaseException

                sleep(5)

                if driver.current_url != 'https://zerojudge.tw/':
                    raise BaseException
            except BaseException as e:
                print(e)
                continue  # 如果登錄失敗，跳過當前帳號，繼續下一個帳號的處理

            # 提交程式
            results = []
            language_upper = language.upper()
            for prob_id in list(submit_program_dict.keys()):
                results = []
                driver.get(f'https://zerojudge.tw/ShowProblem?problemid={prob_id}')

                btn_code = WebDriverWait(driver, wait_max).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success")))
                btn_code.click()

                btn_py = WebDriverWait(driver, wait_max).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[name='language'][value='{language_upper}']")))

                btn_py.click()

                input_code = WebDriverWait(driver, wait_max).until(
                    EC.presence_of_element_located((By.ID, "code")))
                input_code.send_keys(submit_program_dict[prob_id])

                btn_submit = WebDriverWait(driver, wait_max).until(
                    EC.presence_of_element_located((By.ID, "submitCode")))
                btn_submit.click()

                sleep(1)
                table_result = WebDriverWait(driver, wait_max).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "table.table-hover")))
                current_row = WebDriverWait(table_result, wait_max).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))[1]
                sleep(6)
                results.append([])
                for col in WebDriverWait(current_row, wait_max).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
                    results[-1].append(col.text.strip())
            newResult=[]
            for i in range(len(results)):
                if i==1:
                    newResult.append(str(results[i].split('(')[0]))
                if i==2:
                    newResult.append(results[i][:4])
                if i==3 or i==5:
                    newResult.append(results[i])
                if i==4:
                    newResult.append(results[i].lower())

            # 將結果存儲到 CSV 文件中
            if newResult:
                df = pd.DataFrame([newResult])  # 不包含列名
                # 轉換 DataFrame 為字串
                csv_data = df.to_csv(index=False, header=False, encoding='utf-8')  # 使用UTF-8編碼
                # 寫入 CSV 文件
                with open('./crawler/result.csv', 'a', encoding='utf-8') as f:  # 使用UTF-8編碼
                    f.write(csv_data)  # 直接寫入CSV數據
                    f.write('\n')  # 添加換行符
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print(results)
            return results

