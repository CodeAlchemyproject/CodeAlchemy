# 引入所需的模組和套件
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import traceback

def CodeAlchemy_add_problem(problem_id, title, content, enter_description, output_description, example_input, example_output):
    main_url = 'http://123.192.165.145:8081/Login'
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None  # 初始化 driver 變數
    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("disable-infobars")
        os.environ["WDM_ARCH"] = "64" 
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.maximize_window()
        wait_max = 10

        username = 'zero'
        password = '!@#$zerojudge'

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

            if driver.current_url != 'http://123.192.165.145:8081/':
                raise BaseException
            else:
                print("登入成功")
            driver.get('http://123.192.165.145:8081/InsertProblem')

            # 等待標題輸入框出現
            title_input = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'title')))
            title_input.clear()
            title_input.send_keys(title)

            # 切換到 iframe 並輸入 content
            WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.ID, 'mce_0_ifr')))
            driver.switch_to.frame('mce_0_ifr')

            content_area = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))  # 通常編輯器的內容區域會是 <body> 標籤
            content_area.send_keys(content)

            # 切換回主頁面
            driver.switch_to.default_content()

            # 切換到新的 iframe 並輸入 enter_description
            WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.ID, 'mce_13_ifr')))
            driver.switch_to.frame('mce_13_ifr')

            theinput = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
            theinput.send_keys(enter_description)

            # 切換回主頁面
            driver.switch_to.default_content()

            # 切換到另一個 iframe 並輸入 output_description
            WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.ID, 'mce_14_ifr')))
            driver.switch_to.frame('mce_14_ifr')

            theinput = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
            theinput.send_keys(output_description)

            # 切換回主頁面
            driver.switch_to.default_content()

            # 輸入測試數據
            sampleinput = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'sampleinput')))
            sampleinput.send_keys(example_input)

            sampleoutput = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'sampleoutput')))
            sampleoutput.send_keys(example_output)

            # 點擊更新問題按鈕
            update_button = WebDriverWait(driver, wait_max).until(
                EC.element_to_be_clickable((By.NAME, 'updateProblem')))
            update_button.click()

            # 處理測試資料上傳
            infilepattern = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'infilepattern')))
            infilepattern.clear()
            infilepattern.send_keys(f'{problem_id}_##.in')

            outfilepattern = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'outfilepattern')))
            outfilepattern.clear()
            outfilepattern.send_keys(f'{problem_id}_##.out')

            # 找到上傳檔案的 input 元素
            testdatas = WebDriverWait(driver, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'testdatas')))  # 確保這是 <input type="file" multiple="multiple">

            print("找到檔案上傳欄位，準備上傳多個檔案...")

            base_path = os.path.dirname(os.path.abspath(__file__))
            print(f"Base Path: {base_path}")  # 輸出當前文件的絕對路徑
            relative_path = os.path.join(base_path, '.','source', 'testdata', problem_id)
            print(f"Relative Path: {relative_path}")  # 輸出計算出的相對路徑

            # 列出目錄下所有檔案的完整路徑
            file_paths = []
            for root, dirs, files in os.walk(relative_path):
                for file in files:
                    file_paths.append(os.path.join(root, file))

            # 檢查是否找到檔案
            if not file_paths:
                print("未找到任何檔案，請檢查路徑！")
            else:
                # 將所有檔案路徑用分號分隔起來（適用於 Windows）
                all_files = ';'.join(file_paths)
            print(f"找到的檔案: {all_files}")
            testdatas.send_keys(all_files)  # 上傳檔案路徑，使用分號分隔

            # 點擊更新問題按鈕
            uploadFiles = WebDriverWait(driver, wait_max).until(
                EC.element_to_be_clickable((By.ID, 'uploadFiles')))
            uploadFiles.click()    
            sleep(10)
        except Exception as e:
            print(e)
            return []  # 返回空列表，表示登錄失敗
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        return None 
