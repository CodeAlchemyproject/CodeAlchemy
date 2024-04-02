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
def ZJ_submit(prob_id,content):
    # load account information
    with open('account.json', 'r') as file: 
        account = json.load(file)
        
    username = account['username']
    password = account['password']

    # crawler setting
    main_url = 'https://zerojudge.tw/Login'

    s = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.get(main_url)

    wait_max = 10

    # login the website
    try:
        print('\nLogin Automatically ... \n')
        login_area = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-md-4.text-center')))
        login_area = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-horizontal')))

        time.sleep(1)

        input_username = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'account')))
        input_username.send_keys(username)

        time.sleep(1)

        input_password = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.ID, 'passwd')))
        input_password.send_keys(password)

        time.sleep(3)

        iframe = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        driver.switch_to.frame(iframe)

        driver.execute_script("document.querySelector('.recaptcha-checkbox').click();")

        time.sleep(3)

        driver.switch_to.default_content()

        btn_login = WebDriverWait(login_area, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-primary")))
        btn_login.click()

        time.sleep(5)
        
        if driver.current_url != 'https://zerojudge.tw/': raise BaseException

    except BaseException as e:
        print(e)

    # submit the programs
    results = []
    try:
        driver.get(f'https://zerojudge.tw/ShowProblem?problemid={prob_id}')

        btn_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success")))
        btn_code.click()
        
        btn_py = WebDriverWait(driver, wait_max).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='language'][value='PYTHON']")))
        btn_py.click()
        
        input_code = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "code")))
        input_code.send_keys(content)
        
        btn_submit = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.ID, "submitCode")))
        btn_submit.click()
        
        time.sleep(35)
        
        table_result = WebDriverWait(driver, wait_max).until(EC.presence_of_element_located((By.CLASS_NAME, "table.table-hover")))
        current_row = WebDriverWait(table_result, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))[1]
        
        results.append([])
        for col in WebDriverWait(current_row, wait_max).until(EC.presence_of_all_elements_located((By.TAG_NAME, "td"))):
            results[-1].append(col.text.strip())
                
    except BaseException as e:
        print(prob_id, e)

    return results
