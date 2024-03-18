import requests
from bs4 import BeautifulSoup
def submit_code_to_zerojudge(problem_id, language, code):
    # ZeroJudge提交URL
    submission_url = 'https://zerojudge.tw/Solution.api?action=SubmitCode&'

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


# 函式：獲取並打印提交紀錄
def print_submission_records():
    url = "https://zerojudge.tw/Submissions?problemid=a001"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        submission_table = soup.find("table", {"class": "table table-striped table-hover"})
        
        if submission_table:
            rows = submission_table.find_all('tr', {'solutionid': '13502901'})
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all("td")
                solve_id = cols[0].text.strip()
                user_id = cols[1].text.strip()
                problem_id = cols[2].text.strip()
                verdict = cols[4].text.strip()
                execution_time = cols[6].text.strip()
                language = cols[7].text.strip()

                print(f"Submission ID: {solve_id}")
                print(f"User ID: {user_id}")
                print(f"Problem ID: {problem_id}")
                print(f"Verdict: {verdict}")
                print(f"Execution Time: {execution_time}")
                print(f"Language: {language}")
                print()

        else:
            print("Submission table not found.")
    else:
        print("Failed to retrieve submission records.")

# 主程式入口
if __name__ == "__main__":
    print_submission_records()


