# 引入所需的模組和套件

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

def CodeAlchemy_submit(title):
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

        username = 'TestCase2024'
        password = 'TestCase2024'

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
    # # 輸入搜索關鍵字
    searchword_input = driver.find_element_by_name('searchword')
    searchword_input.send_keys(title)

    # 找到搜索表單並提交
    search_form = searchword_input.find_element_by_xpath('ancestor::form')
    search_form.submit()

    # 等待新頁面載入完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table.table-hover')))

    # 獲取表格中的第一個連結
    table = driver.find_element_by_class_name('table.table-hover')
    first_a_element = table.find_element_by_xpath('.//a[contains(@href, "ShowProblem?problemid=")]')

    # 點擊第一個連結
    first_a_element.click()

    # 等待新頁面載入完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))

    # 獲取新頁面的內容並輸出
    print(driver.page_source)
CodeAlchemy_submit('哈囉')
