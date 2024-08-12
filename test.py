import os
import requests

# 將 YOUR_API_KEY 替換為你的實際 API 金鑰
API_KEY = "AIzaSyAgXhsExTg7jfS_e5VnWyAf7oG8e8mvtNc"
API_URL = "https://api.gemini.com/v1/generate"

def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gemini-pro-1.5",
        "prompt": prompt,
        "max_tokens": 100,  # 調整生成文本的最大長度
        "temperature": 0.7,   # 調整生成文本的隨機性
    }
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

while True:
    user_input = input("請輸入你的文字：")
    if user_input.lower() == "exit":
        break
    response_text = generate_text(user_input)
    print("Gemini 回應：", response_text)