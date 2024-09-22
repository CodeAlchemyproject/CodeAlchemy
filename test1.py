# 引入所需的模組和套件

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

def CodeAlchemy_submit():
    # crawler setting
    main_url = 'http://123.192.165.145:8081/Login'
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    driver = None  # 初始化 driver 變數
    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("disable-infobars")

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
        except BaseException as e:
            print(e)
            return []  # 返回空列表，表示登錄失敗
    except:
        None
CodeAlchemy_submit()
