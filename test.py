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
from crawler.add_problem import CodeAlchemy_add_problem

CodeAlchemy_add_problem('1002'
                 ,'數字排序器'
                 ,"給定一串整數序列，請設計一個程式能將這些數字依從小到大的順序排序，並且輸出排序後的結果。"
                 ,'輸入的第一行包含一個正整數 N，代表序列中有 N 個數字（1 ≤ N ≤ 100）。接著，第二行包含 N 個用空格分隔的整數，這些整數的範圍為 -1000 到 1000。'
                 ,'輸出排序後的整數序列，所有數字須以空格分隔。'
                 ,'''5
3 -1 0 99 -100
'''
                ,'-100 -1 0 3 99'
                )
# from crawler import submit
# submit.CodeAlchemy_submit('da2b80_CA-a001.py','17','哈囉')
