import glob
import os


language='java'
username='yyyiii'
# 定義語言對應的文件擴展名字典
file_extensions = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp'
}
# 讀取所有檔案
file_extension = file_extensions.get(language, '')
print(file_extension)
submit_program_dict = dict()
files = glob.glob(f'./爬蟲/src/{username}/*.py')  # 根據副檔名讀取檔案
for file_name in files:
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        submit_program_dict[os.path.basename(file_name).split('.')[0]] = content