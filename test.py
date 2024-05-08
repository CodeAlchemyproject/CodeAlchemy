#code = '''print(f'hello, {input()}')'''
import requests

# 定義代理伺服器的IP地址和端口號
proxy_ip = '60.199.29.42'
proxy_port = '8111'

# 定義代理字典
proxy = {
    'http': f'http://{proxy_ip}:{proxy_port}',
    'https': f'https://{proxy_ip}:{proxy_port}'
}

# 發送帶有代理的GET請求
response = requests.get('https://www.google.com.tw/', proxies=proxy)

# 輸出回應內容
print(response.text)
