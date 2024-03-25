from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置浏览器驱动程序的路径
driver_path = 'C:\\Users\\My_User\\Documents\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# 创建一个 Chrome 服务对象
service = Service(driver_path)

# 创建一个 Chrome WebDriver 对象，指定服务
driver = webdriver.Chrome(service=service)

# 目标 URL
url = 'https://zerojudge.tw/Login'
driver.get(url)

# 找到帐号和密码的输入框元素，并输入数据
account = driver.find_element(By.CSS_SELECTOR, 'input.form-control#account[type=text]')
account.send_keys('codealchemyproject@gmail.com')

passwd = driver.find_element(By.CSS_SELECTOR, 'input.form-control#passwd[type=password]')
passwd.send_keys('10956CodeAlchemy')

# 等待 reCAPTCHA 加载完毕
wait = WebDriverWait(driver, 20)
submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))

# 点击提交按钮
submit_button.click()

# 等待登录结果
try:
    wait.until(EC.url_to_be('https://zerojudge.tw/Index'))
    print('登录成功！')
except:
    print('登录失败！')

# 关闭浏览器
driver.quit()
