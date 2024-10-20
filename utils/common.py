import re
import subprocess
import time
import psutil
import random
import string
def ZJ_translated_return_abbreviation(score):
    if score.startswith("AC"):
       message='通過'
       ensue='Accepted'
    elif score.startswith("NA"):
        message = "未通過所有測資點"
        ensue='Not Accept'
    elif score.startswith("WA"):
        message = '答案錯誤'
        ensue='Wrong Answer'
    elif score.startswith("TLE"):
        message = '執行超過時間限制'
        ensue='Time Limit Exceed'
    elif score.startswith("MLE"):
        message = "程序執行超過記憶體限制"
        ensue='Memory Limit Exceed'
    elif score.startswith("OLE"):
        message = "程序輸出檔超過限制"
        ensue='Output Limit Exceed'
    elif score.startswith("RE"):
        message = "執行時錯誤"
        ensue='Runtime Error'
    elif score.startswith("RF"):
        message = "使用了被禁止使用的函式"
        ensue='Restricted Function'
    elif score.startswith("CE"):
        message = "編譯錯誤"
        ensue='Compile Error'
    elif score.startswith("SE"):
        message = "系統錯誤"
        ensue='System Error'
    else:
        message = "未知錯誤"
        ensue="Unknown Error"
    return message,ensue
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

#分頁功能
def paginate(data,page, per_page):
    offset = (page - 1) * per_page
    return data[offset: offset + per_page],len(data)

#修改帶LaTex字串
def LaTex_double_dollars(input_string):
    output_string = ''
    for char in input_string:
        if char == '$':
            output_string += '$$'
        else:
            output_string += char
    return output_string


def random_string():
    # 定義字母和數字集合
    letters = string.ascii_letters  # 包括大寫和小寫字母
    digits = string.digits  # 包括數字 0-9
    all_chars = letters + digits  # 所有可能的字符

    # 確保以字母開頭
    first_char = random.choice(letters)

    # 隨機生成其餘五個字符
    remaining_chars = ''.join(random.choices(all_chars, k=5))

    # 拼接成完整的六位字符
    random_string = first_char + remaining_chars

    return random_string

def remove_chars(s):
    # 確保字串長度至少為3，否則返回原字串
    if len(s) > 2:
        return s[1:-2]  # 去掉第一個字和最後兩個字
    else:
        return s  # 如果字串長度不足，返回原字串