# from utils.common import random_string
# from crawler.registration import TIOJ_registration,ZeroJudge_registration, add_account
# number=random_string()+"17"
# TIOJ_registration(number)
# ZeroJudge_registration('PGlEzN17')
# # 呼叫新增帳戶函式
# add_account(number, number, './crawler/account.json')
import re
from crawler.submit import TIOJ_submit,ZeroJudge_submit
from utils.common import ZJ_translated_return_abbreviation
print(TIOJ_submit('bfc834_TIOJ-1001.py',str(17)))


#print(ZeroJudge_submit('Gawa20_ZJ-a001.py',str(17)))
# number='17'
# results=[['13955725', 'PGlEzN17 (PGlEzN17)', 'a001. 哈囉 -- Brian Kernighan', 'AC (17ms, 3.3MB)', 'PYTHON', '2024-05-25 15:09']]
# newResult = []
# for i in range(len(results[0])):  # 遍歷結果的每一列
#     if i == 1:
#         newResult.append(number + ',')
#     elif i == 2:
#         newResult.append('ZJ-' + results[0][i][:4])
#     elif i == 3:
#         if results[0][i].startswith('AC'):
#             message, ensue = ZJ_translated_return_abbreviation(results[0][i])
#             newResult.append(ensue + ',')
#             if ensue == 'Accepted':
#                 match = re.search(r'\((\d+ms),\s([\d.]+MB)\)', results[0][i])
#                 if match:
#                     run_time = match.group(1)
#                     memory = match.group(2)
#                     newResult.append(run_time + ',')
#                     newResult.append(memory + ',')
#     elif i == 5:
#         newResult.append(results[0][i])
#     elif i == 4:
#         newResult.append(results[0][i].lower())
# print(newResult)