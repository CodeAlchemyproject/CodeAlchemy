import os
import random
import shutil

def distribute_files(source_folder, target_folders):
    files = os.listdir(source_folder)
    num_files = len(files)
    num_folders = len(target_folders)
    
    files_per_folder = num_files // num_folders
    remainder = num_files % num_folders
    
    # 對目標文件夾進行隨機排序
    random.shuffle(target_folders)
    
    for i, folder in enumerate(target_folders):
        files_to_copy = files[i * files_per_folder : (i + 1) * files_per_folder]
        if i < remainder:
            files_to_copy.append(files[num_folders * files_per_folder + i])
        for file_name in files_to_copy:
            source_file_path = os.path.join(source_folder, file_name)
            target_file_path = os.path.join(folder, file_name)
            shutil.copy(source_file_path, target_file_path)
    
    # 刪除來源文件夾中的文件
    for file_name in files:
        source_file_path = os.path.join(source_folder, file_name)
        os.remove(source_file_path)
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




