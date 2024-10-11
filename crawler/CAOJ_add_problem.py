# 引入所需的模組和套件
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 匯入 Keys 模組來模擬按鍵動作
import pandas as pd
from time import sleep
import os
import glob
import traceback

def CodeAlchemy_add_problem(title, content, enter_description, output_description, example_input, example_output,):
    # crawler setting
    main_url = 'http://123.192.165.145:8081/Login'
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None  # 初始化 driver 變數
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("disable-infobars")
        os.environ["WDM_ARCH"] = "64" 
        driver = webdriver.Chrome(options=chrome_options)
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

            title_input = WebDriverWait(login_area, wait_max).until(
                EC.presence_of_element_located((By.NAME, 'title')))
            # 清空該輸入框的值
            title_input.clear()
            title_input.send_keys(title)
            # 切換到 iframe
            WebDriverWait(login_area, wait_max).until(
                EC.presence_of_element_located((By.ID, 'mce_0_ifr'))
            )
            login_area.switch_to.frame('mce_0_ifr')

            # 在 iframe 中找到編輯器內容區域並輸入內容
            content_area = WebDriverWait(login_area, wait_max).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))  # 通常編輯器的內容區域會是 <body> 標籤
            )
            content_area.send_keys(content)  # 輸入內容

            # 切換回主頁面
            login_area.switch_to.default_content()

        except BaseException as e:
            print(e)
            return []  # 返回空列表，表示登錄失敗
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        return None