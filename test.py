# from crawler.registration import ZeroJudge_registration
# from crawler.submit import ZeroJudge_Submit
# ZeroJudge_registration('17')
# ZeroJudge_Submit('a001.py')
# from crawler.submit import TIOJ_submit
# TIOJ_submit('aaaaaa-TIOJ-1001.py','TestCase2024')
# from crawler.get_problem import get_TIOJ_All_Problem
# get_TIOJ_All_Problem()
# from crawler.registration import TIOJ_registration,ZeroJudge_registration
# TIOJ_registration('1')
# ZeroJudge_registration('1')
#題目
from datetime import datetime
import os
import re
import uuid
from flask import request, session
from crawler.submit import TIOJ_submit, ZeroJudge_Submit
from utils import db


