import subprocess
import time
import psutil

# 評測函式，接受題目資料和使用者提交的程式碼
def evaluate(problem, user_code):
    try:
        # 使用 subprocess 執行程式碼
        process = subprocess.Popen(['python3', '-c', user_code],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        # 將題目的輸入作為 stdin 傳遞
        process.stdin.write(problem["example_inputs"])
        process.stdin.close()  # 關閉標準輸入，以便程式碼知道已經結束輸入
        # 開始計時
        start_time = time.time()
        # 將題目的輸入提供給使用者程式碼
        stdout, stderr = process.communicate(timeout=5)
        # 結束計時
        end_time = time.time()
        # 計算程式碼的執行時間
        execution_time = end_time - start_time
        
        # 獲取程式碼執行期間的記憶體使用情況
        try:
            process_memory_usage = psutil.Process(process.pid).memory_info().rss / 1024 / 1024  # 轉換為 MB
        except psutil.NoSuchProcess:
            process_memory_usage = 0
        
        # 檢查是否有執行時錯誤
        if process.returncode != 0:
            if "out of" in stderr:
                return False, "執行時錯誤：記憶體不足", execution_time, process_memory_usage
            elif "TimeLimit" in stderr:
                return False, "執行時錯誤：執行超過時間限制", execution_time, process_memory_usage
            else:
                return False, "執行時錯誤：" + stderr, execution_time, process_memory_usage
        return True, "執行成功", execution_time, process_memory_usage
    except subprocess.TimeoutExpired:
        return False, "執行超過時間限制", None, None
    except Exception as e:
        return False, "發生未知錯誤：" + str(e), None, None
