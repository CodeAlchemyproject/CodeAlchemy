import requests

def submit_code_to_zerojudge(problem_id, language, code):
    # ZeroJudge提交URL
    submission_url = 'https://zerojudge.tw/Solution.api'

    # 構建提交的數據
    data = {
        'problemid': problem_id,
        'language': language,
        'code': code
    }

    # 發送POST請求
    response = requests.post(submission_url, data=data)

    # 檢查響應狀態碼
    if response.status_code == 200:
        print('代碼提交成功！')
        # 如果需要，你可以進一步處理響應的內容
        # 例如，檢查提交結果，獲取評分結果等
    else:
        print('代碼提交失敗！')

# 使用者輸入問題ID、編程語言和代碼內容
problem_id = input('請輸入問題ID：')
language = input('請輸入編程語言：')
code = input('請輸入代碼內容：')

# 提交代碼到ZeroJudge評分系統
submit_code_to_zerojudge(problem_id, language, code)
