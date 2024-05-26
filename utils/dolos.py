import requests # pip install requests
import zipfile
import os
import uuid
import glob
def search_file(problem_id):
   file_to_compress = '../source'
   pattern = pattern = f'*_{problem_id}*'
   files = glob.glob(os.path.join(file_to_compress, pattern))
   return files
def create_zip(problem_id):
    # 指定要壓縮的檔案
   file_to_compress = 'source\\a2e64f_TIOJ-1001.py'
   # 指定輸出 Zip 檔案的路徑
   output_zip_path = f'dolos/{uuid.uuid4()}_{problem_id}.zip'
   # 確保輸出的目錄存在
   os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)
   # 創建一個新的 Zip 檔案
   with zipfile.ZipFile(output_zip_path, 'w') as zipf:
      # 將指定檔案添加到 Zip 檔案中
      zipf.write(file_to_compress, os.path.basename(file_to_compress))
   return(output_zip_path.split('/')[1],output_zip_path)

def submit_to_dolos(name, zipfile_path):
   """
   Submit a ZIP-file to the Dolos API for plagiarism detection
   and return the URL where the resulting HTML report can be found.
   """
   response = requests.post(
      'https://dolos.ugent.be/api/reports',
      files = { 'dataset[zipfile]': open(zipfile_path, 'rb') },
      data = { 'dataset[name]': name }
   )
   json = response.json()
   return json["html_url"]