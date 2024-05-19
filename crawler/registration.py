# 引入所需的模組和套件
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import traceback
import json

def add_account(username, password, json_file):
    # 讀取JSON檔案
    with open(json_file, 'r') as f:
        data = json.load(f)
    # 新增帳戶
    data['account'].append([username, password])
    # 寫入更新後的資料到JSON檔案中
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def ZeroJudge_registration(number):
    main_url = 'https://zerojudge.tw/InsertUser'
     # 禁用瀏覽器彈窗避免預設路徑載入失敗
    driver = None  # 初始化 driver 變數
    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        # 將擴充套件放入至Webdriver的開啟網頁內容
        
        prefs = {'profile.default_content_setting_values': {'notifications': 2}}
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument(f'user-agent={user_agent}')
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
        #註冊ZeroJudge帳號
        driver.get(main_url)
        # 生成隨機字串，第一個字母為英文字母
        random_code = str(uuid.uuid4())[:6]  # 取uuid的前5位作為隨機字串
        # 如果第一個字元不是英文字母，則重新生成，直到第一個字元為英文字母
        while not random_code[0].isalpha():
            random_code = str(uuid.uuid4())[:6]
        #帳號
        number = random_code + '-' +number
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "account")))
        input_code.send_keys(number)
        user_name=number.split('-')[0]
        sleep(2)
        #密碼
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "passwd")))
        input_code.send_keys(number)
        password=number.split('-')[0]
        sleep(2)
        #確認密碼
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "passwd2")))
        input_code.send_keys(number)
        sleep(2)
        #公開暱稱
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "username")))
        input_code.clear()
        input_code.send_keys(number)
        sleep(2)
        #真實姓名
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "truename")))
        input_code.send_keys(number)
        sleep(2)
        #電子郵件
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.NAME, "email")))
        input_code.clear()
        input_code.send_keys(f'{user_name}@gmail.com')
        sleep(2)

        #提交
        for i in range(60):
            sleep(1)
            try:
                btn_submit = WebDriverWait(driver, wait_max).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[2]/form/div[10]/button')))
                btn_submit.click()
                break
            except:
                pass
        sleep(5)
        btn_Okay = WebDriverWait(driver, wait_max).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[3]/div/div/button')))
        btn_Okay.click()
        driver.implicitly_wait(5)
        driver.quit()
        # 呼叫新增帳戶函式
        add_account(user_name, password, './crawler/account.json')
    
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

def TIOJ_registration(number):
    main_url = 'https://tioj.ck.tp.edu.tw/users/sign_up'
     # 禁用瀏覽器彈窗避免預設路徑載入失敗
    driver = None  # 初始化 driver 變數
    try:
        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        # 將擴充套件放入至Webdriver的開啟網頁內容
        
        prefs = {'profile.default_content_setting_values': {'notifications': 2}}
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument(f'user-agent={user_agent}')
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
        #註冊TIOJ帳號
        driver.get(main_url)
        # 生成隨機字串，第一個字母為英文字母
        random_code = str(uuid.uuid4())[:6]  # 取uuid的前5位作為隨機字串
        # 如果第一個字元不是英文字母，則重新生成，直到第一個字元為英文字母
        while not random_code[0].isalpha():
            random_code = str(uuid.uuid4())[:6]
        #帳號
        mail=number
        number = random_code + '-' +number
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_username")))
        input_code.send_keys(number)
        sleep(2)
        #密碼
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_password")))
        input_code.send_keys(number)
        sleep(2)
        #確認密碼
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_password_confirmation")))
        input_code.send_keys(number)
        sleep(2)
        #公開暱稱
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_nickname")))
        input_code.clear()
        input_code.send_keys(number)
        sleep(2)
        #真實姓名
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_name")))
        input_code.send_keys(number)
        sleep(2)
        #電子郵件
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_email")))
        input_code.clear()
        input_code.send_keys(f'{mail}@gmail.com')
        sleep(2)
        #學校
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_school")))
        input_code.clear()
        input_code.send_keys(number)
        sleep(2)
        #畢業年
        input_code = WebDriverWait(driver, wait_max).until(
        EC.presence_of_element_located((By.ID, "user_gradyear")))
        input_code.clear()
        input_code.send_keys(114)
        sleep(2)
    
        #提交
        btn_submit = WebDriverWait(driver, wait_max).until(
            EC.presence_of_element_located((By.NAME, 'commit')))
        btn_submit.click()

        sleep(5)
        driver.quit()
        # 呼叫新增帳戶函式
        add_account(number, number, './crawler/account.json')

    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()


    





    


