# 引入所需的模組和套件
from datetime import datetime
import re
from flask import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
import os
import glob
import traceback

from utils.common import ZJ_translated_return_abbreviation
def test_submit():
    chrome_options = webdriver.ChromeOptions()
    s = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=s, options=chrome_options)
    # 登入頁面的 URL
    url = 'http://123.192.165.145:8081/Login'

    # 打開網頁
    driver.get(url)

    # 等待登入表單元素載入完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'account')))

    # 找到帳號和密碼輸入框
    account_input = driver.find_element_by_id('account')
    passwd_input = driver.find_element_by_id('passwd')

    if account_input and passwd_input:
        # 輸入帳號和密碼
        account_input.send_keys('zero')
        passwd_input.send_keys('!@#$zerojudge')

        # 找到登入按鈕並點擊
        login_button = driver.find_element_by_css_selector('button.btn.btn-primary')
        login_button.click()

        # 等待登入完成，這裡可以根據需要加入等待條件，例如等待特定元素載入完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'searchword')))

        # # 輸入搜索關鍵字
        # searchword_input = driver.find_element_by_name('searchword')
        # searchword_input.send_keys(title)

        # # 找到搜索表單並提交
        # search_form = searchword_input.find_element_by_xpath('ancestor::form')
        # search_form.submit()

        # # 等待新頁面載入完成
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table.table-hover')))

        # # 獲取表格中的第一個連結
        # table = driver.find_element_by_class_name('table.table-hover')
        # first_a_element = table.find_element_by_xpath('.//a[contains(@href, "ShowProblem?problemid=")]')

        # # 點擊第一個連結
        # first_a_element.click()

        # # 等待新頁面載入完成
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))

        # # 獲取新頁面的內容並輸出
        # print(driver.page_source)
    driver.quit()

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
        chrome_options.add_argument("disable-infobars")
        # 強制指定為 win64 版本
        os.environ["WDM_ARCH"] = "64" 
        driver = webdriver.Chrome()
        driver.maximize_window()
        wait_max = 10

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
            if acc[0][0-len(str(number)):]==number:
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
                newResult=[]
                f.write(number + ",")
                newResult.append(number)

                f.write('TIOJ-'+file_key + ",")
                newResult.append(f'TIOJ-{file_key}')

                f.write(csv_data.strip() + ",")
                for i in csv_data.strip().split(','):
                    newResult.append(i)

                f.write(language+ ",")
                newResult.append(language)
                now_time=str(datetime.now())# 轉換為字符串

                f.write(now_time) 
                newResult.append(now_time)
                f.write('\n')

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

        return newResult

def ZeroJudge_submit(file_name, number):
    # crawler setting
    main_url = 'https://zerojudge.tw/Login'
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None  # 初始化 driver 變數
    results = []  # 初始化 results 變數
    newResult = []  # 初始化 newResult 變數

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_extension('./crawler/extension/reCAPTCHA_extension.crx')
        chrome_options.add_extension('./crawler/extension/vpn_extension_Touch.crx')
        chrome_options.add_argument("disable-infobars")
        os.environ["WDM_ARCH"] = "64" 
        driver = webdriver.Chrome(options=chrome_options)
        print(driver)
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
            else:
                continue

            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                file_key = os.path.basename(file_name)[7:].replace("ZJ-", "").split('.')[0]
                submit_program_dict[file_key] = content

        with open('./crawler/account.json', 'r') as file:
            accounts = json.load(file)['account']

        username = None
        password = None

        for acc in accounts:
            if acc[0][0-len(str(number)):] == number:
                username = acc[0]
                password = acc[1]
                break

        if not username or not password:
            username = "TestCase2024"
            password = "TestCase2024"

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
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary')))
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
            return []  # 返回空列表，表示登錄失敗

        results = []
        language_upper = language.upper()
        for prob_id in list(submit_program_dict.keys()):
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
            row_data = []
            for col in WebDriverWait(current_row, wait_max).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
                row_data.append(col.text.strip())
            results.append(row_data)

        newResult = []
        for i in range(len(results[0])):  # 遍歷結果的每一列
            if i == 1:
                newResult.append(int(number))
            elif i == 2:
                newResult.append('ZJ-' + results[0][i][:4])
            elif i == 3:
                if results[0][i].startswith('AC'):
                    message, ensue = ZJ_translated_return_abbreviation(results[0][i])
                    newResult.append(ensue)
                    if ensue == 'Accepted':
                        match = re.search(r'\((\d+ms),\s([\d.]+MB)\)', results[0][i])
                        if match:
                            run_time = match.group(1)
                            memory = match.group(2)
                            newResult.append(run_time)
                            newResult.append(memory)
                    else:
                        newResult.append('0')
                        newResult.append('0')
            elif i == 5:
                newResult.append(results[0][i])
            elif i == 4:
                newResult.append(results[0][i].lower())

        if newResult:
            df = pd.DataFrame([newResult])
            csv_data = df.to_csv(index=False, header=False, encoding='utf-8').strip()
            with open('./crawler/result.csv', 'a', encoding='utf-8') as f:
                f.write(csv_data)
                f.write('\n')

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        return newResult