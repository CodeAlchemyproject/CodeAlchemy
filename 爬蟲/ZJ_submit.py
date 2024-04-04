# 引入所需的模組和套件
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import time
import os
import glob
import json
import threading


def process_account(username, password, language):
    # crawler setting
    main_url = 'https://zerojudge.tw/Login'
    language=language
    s = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_extension('./爬蟲/reCAPTCHA_extension.crx')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    wait_max = 10
    # 定義語言對應的文件擴展名字典
    file_extensions = {
        'python': '.py',
        'java': '.java',
        'c': '.c',
        'cpp': '.cpp'
    }
    # 讀取所有Python檔案
    submit_program_dict = dict()
    py_files = glob.glob(f'./爬蟲/src/{username}/*.py')
    for file_name in py_files:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            submit_program_dict[os.path.basename(file_name).split('.')[0]] = content

    
    driver.get(main_url)

    # 登錄網站
    try:
        print('\n自動登錄中... \n')
        login_area = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-md-4.text-center')))
        login_area = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-horizontal')))

        time.sleep(1)

        input_username = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'account')))
        input_username.send_keys(username)

        time.sleep(1)

        input_password = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'passwd')))
        input_password.send_keys(password)
        
        time.sleep(3)
        
        for i in range(60):
            time.sleep(1)
            try:
                btn_login = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-primary')))
                btn_login.click()
                break
            except: pass
        else: raise BaseException
        
        time.sleep(5)
        
        if driver.current_url != 'https://zerojudge.tw/': raise BaseException

    except BaseException as e:
        print(e)
        input('\n= = = = = 請手動登錄網站後按下ENTER = = = = =\n')
    
    # 提交程式
    for prob_id in list(submit_program_dict.keys()):
        results = []
        try:
            driver.get(f'https://zerojudge.tw/ShowProblem?problemid={prob_id}')

            btn_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success")))
            btn_code.click()
            
            btn_py = WebDriverWait(driver, wait_max).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='language'][value='PYTHON']")))
            btn_py.click()
            
            input_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "code")))
            input_code.send_keys(submit_program_dict[prob_id])
            
            btn_submit = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "submitCode")))
            btn_submit.click()
            
            time.sleep(35)
            
            table_result = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "table.table-hover")))
            current_row = WebDriverWait(table_result, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))[1]
            
            results.append([])
            for col in WebDriverWait(current_row, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
                results[-1].append(col.text.strip())
            return (results)
        except BaseException as e:
            print(prob_id, e)
    driver.quit()
    
   

