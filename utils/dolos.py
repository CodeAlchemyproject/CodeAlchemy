import requests
import zipfile
import os
import uuid
import glob

def create_zip(problem_id):
    pattern = f'*_{problem_id}*'
    files = glob.glob(os.path.join('source', pattern))
    
    # 指定輸出 Zip 檔案的路徑
    output_zip_path = f'dolos/{uuid.uuid4()}_{problem_id}.zip'
    
    # 確保輸出的目錄存在
    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)
    
    # 創建一個新的 Zip 檔案
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    
    return (os.path.basename(output_zip_path), output_zip_path)

def submit_to_dolos(name, zipfile_path):
    """
    Submit a ZIP-file to the Dolos API for plagiarism detection
    and return the URL where the resulting HTML report can be found.
    """
    # 提交 ZIP 檔案到 Dolos API
    with open(zipfile_path, 'rb') as zip_file:
        response = requests.post(
            'http://123.192.165.145:3000/reports',
            files={'dataset[zipfile]': zip_file},
            data={'dataset[name]': name}
        )
    
    # 解析 JSON 響應
    json_response = response.json()
    
    # 刪除已提交的 ZIP 檔案
    try:
        os.remove(zipfile_path)
        print(f'已刪除檔案: {zipfile_path}')
    except Exception as e:
        print(f'刪除檔案 {zipfile_path} 時發生錯誤: {e}')
    
    # 返回 HTML 報告的 URL
    return json_response["html_url"]
