# from crawler.registration import ZeroJudge_registration
# from crawler.submit import ZeroJudge_Submit
# ZeroJudge_registration('17')
# ZeroJudge_Submit('a001.py')
# from crawler.submit import TIOJ_submit
# TIOJ_submit('aaaaaa-TIOJ-1001.py','TestCase2024')
# from crawler.get_problem import TIOJ_get_problem,get_TIOJ_All_Problem
# get_TIOJ_All_Problem()
from utils.common import random_string
from crawler.registration import TIOJ_registration,ZeroJudge_registration
for i in range(1,20):
    number=random_string()+str(i)
    TIOJ_registration(number)
    ZeroJudge_registration(number)


