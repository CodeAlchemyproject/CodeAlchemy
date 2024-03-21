from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def login_to_zerojudge(username, password):
    login_url = "https://zerojudge.tw/Login"

    # 启动浏览器
    driver = webdriver.Edge()  # 需要下载并安装 Chrome 驱动，或者使用其他浏览器驱动
    driver.get(login_url)

    # 等待页面加载完成
    time.sleep(2)

    # 输入用户名和密码
    username_field = driver.find_element_by_id("UserName")
    username_field.send_keys(username)
    password_field = driver.find_element_by_id("Password")
    password_field.send_keys(password)

    # 提交登录表单
    login_button = driver.find_element_by_id("login")
    login_button.click()

    # 等待登录完成
    time.sleep(2)

    # 获取登录后的页面内容
    logged_in_page = driver.page_source

    # 关闭浏览器
    driver.quit()

    # 查找隐藏字段中的 CSRF 令牌
    csrf_token_start = logged_in_page.find('__RequestVerificationToken')
    if csrf_token_start != -1:
        csrf_token_value = logged_in_page[csrf_token_start:].split('"')[2]
        print("CSRF 令牌:", csrf_token_value)
        return csrf_token_value
    else:
        print("找不到 CSRF 令牌。")
        return None

# 使用示例
username = 'codealchemyproject@gmail.com'  # 修改为你的用户名
password = '10956010CodeAlchemy'  # 修改为你的密码
csrf_token = login_to_zerojudge(username, password)
