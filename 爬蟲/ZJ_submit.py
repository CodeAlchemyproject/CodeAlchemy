from selenium import webdriver

# 设置浏览器驱动程序的路径
driver_path = "C:\\Users\\My_User\\Documents\\msedgedriver.exe"

# 创建一个 Edge WebDriver 对象
options = webdriver.EdgeOptions()
options.binary_location = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
driver = webdriver.Edge(options=options)

# 目标 URL
url = 'https://zerojudge.tw/Login'
driver.get(url)

# 根据 id 定位账号输入框，并输入账号
account_input = driver.find_element_by_id('account')
account_input.send_keys('codealchemyproject@gmail.com')

# 根据 id 定位密码输入框，并输入密码
password_input = driver.find_element_by_id('passwd')
password_input.send_keys('10956CodeAlchemy')

# 关闭浏览器
driver.quit()
