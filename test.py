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
