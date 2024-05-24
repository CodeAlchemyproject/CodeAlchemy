# from utils.common import random_string
# from crawler.registration import TIOJ_registration,ZeroJudge_registration, add_account
# number=random_string()+"17"
# TIOJ_registration(number)
# ZeroJudge_registration('PGlEzN17')
# # 呼叫新增帳戶函式
# add_account(number, number, './crawler/account.json')
from crawler.submit import TIOJ_submit,ZeroJudge_submit
TIOJ_submit('bfc834_TIOJ-1001.py',str(17))
