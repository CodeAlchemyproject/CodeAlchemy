import subprocess
import time

# 評測函式，接受題目資料和使用者提交的程式碼
def evaluate(problem, user_code):
    try:
        # 假設題目是使用標準輸入和輸出的問題
        input_data = problem['sample_input']
        output_data = problem['sample_output']
        # 使用 subprocess 執行程式碼
        process = subprocess.Popen(['python3', '-c', user_code],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        # 開始計時
        start_time = time.time()
        # 將題目的輸入提供給使用者程式碼
        stdout, stderr = process.communicate(input_data, timeout=5)
        # 結束計時
        end_time = time.time()
        # 計算程式碼的執行時間
        execution_time = end_time - start_time
        # 檢查是否有執行時錯誤
        if process.returncode != 0:
            if "out of" in stderr:
                return False, "執行時錯誤：記憶體不足", execution_time
            elif "TimeLimit" in stderr:
                return False, "執行時錯誤：執行超過時間限制", execution_time
            else:
                return False, "執行時錯誤：" + stderr, execution_time
        # 檢查程式碼的輸出是否正確
        if stdout.strip() == output_data.strip():
            return True, "答案正確", execution_time
        else:
            return False, "答案錯誤", execution_time
    except subprocess.TimeoutExpired:
        return False, "執行超過時間限制", None
    except Exception as e:
        return False, "發生未知錯誤：" + str(e), None

# 使用示例
problem = {
    "id": 1,
    "title": "A+B Problem",
    "sample_input": "1 2\n",
    "sample_output": "3\n"
}
user_code = """
a, b = map(int, input().split())
print(a + b)
"""
result, message, execution_time = evaluate(problem, user_code)
if result:
    print(message)
    execution_time_ms = execution_time * 1000
    print("執行時間：", round(execution_time_ms, 4), "毫秒")
else:
    print(message)
