import os
import time

def process_account():
    # 在這裡實現你的 process_account() 函式的內容
    print("Processing accounts...")

def monitor_source_folder():
    source_folder = './source'
    while True:
        # 監測 source 資料夾是否有新檔案
        files = os.listdir(source_folder)
        if files:
            print("New file detected:", files)
            # 呼叫 process_account() 函式來處理新檔案
            process_account()
            # 處理完畢後，清空 source 資料夾
            for file in files:
                os.remove(os.path.join(source_folder, file))
        # 暫停一段時間後再次檢查
        time.sleep(5)

if __name__ == "__main__":
    monitor_source_folder()
