import threading
from crawler import registration 
from utils.common import  random_string
number=random_string()+str(18)
# 使用 threading 並行執行 TIOJ 和 ZeroJudge 註冊
t1 = threading.Thread(target=registration.TIOJ_registration, args=(number,))
t2 = threading.Thread(target=registration.ZeroJudge_registration, args=(number,))
# 開始執行這兩個線程
t1.start()
t2.start()
# 等待這兩個線程執行完畢
t1.join()
t2.join()
# 執行新增帳戶操作
registration.add_account(number, number, './crawler/account.json')