from utils.analyse import find_best_code, gemini_api_analyse

problem_id='CAOJ-1002'
user_id=17
l=find_best_code(problem_id,user_id)
print(gemini_api_analyse(l))





