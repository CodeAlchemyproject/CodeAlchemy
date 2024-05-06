import subprocess
import time
import psutil

def evaluate(user_code, problem):
    # 啟動子進程執行用戶代碼
    start_time = time.time()  # 開始計時
    process = subprocess.Popen(['python', '-c', user_code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 向子進程的stdin寫入範例輸入
    process.stdin.write(problem['example_input'].encode())
    process.stdin.close()  # 關閉stdin
    
    # 在進程結束前獲取記憶體使用量
    try:
        memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 * 1024)  # 轉換為MB
    except psutil.NoSuchProcess:
        memory_usage = 0  # 如果找不到進程，將記憶體使用量設置為0
    
    # 獲取子進程的輸出和錯誤信息
    stdout, stderr = process.communicate()
    end_time = time.time()  # 結束計時
    
    # 計算執行時間
    execution_time = end_time - start_time
    
    # 檢查輸出是否符合預期
    result = stdout.decode().strip() == problem['example_output']
    
    return result, stderr.decode(), execution_time, memory_usage


