# # 單個純文字
# import json
# import requests
# api_key='AIzaSyAgXhsExTg7jfS_e5VnWyAf7oG8e8mvtNc'
# url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}'
# headers = {'Content-Type': 'application/json'}
# data = {
#     "contents": [
#         {
#             "parts": [{"text": "你可以幫我分類OnlineJudge上的題目類型嗎,我會可以題目說明以及範例輸入輸出"}]
#         }
#     ]
# }
# response = requests.post(url, headers=headers, json=data)
# print(f"response status_code: {response.status_code}")
# print(json.dumps(response.json(), indent=4, ensure_ascii=False))
# from crawler.submit import CodeAlchemy_submit
# CodeAlchemy_submit('da2b80_CA-a001.py','17','哈囉')

# 讀取第一行的數字，代表有多少個數字需要排序
n = int(input().strip())

# 讀取第二行，並將數字分割成陣列
numbers = list(map(int, input().strip().split()))

# 排序數字
sorted_numbers = sorted(numbers)

# 將排序後的數字輸出，數字之間用空格分隔
print(" ".join(map(str, sorted_numbers)))