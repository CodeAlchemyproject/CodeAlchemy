import requests # pip install requests

def submit_to_dolos(name, zipfile_path):
   """
   Submit a ZIP-file to the Dolos API for plagiarism detection
   and return the URL where the resulting HTML report can be found.
   """
   response = requests.post(
      'http://120.97.27.246:8080/api',
      files = { 'dataset[zipfile]': open(zipfile_path, 'rb') },
      data = { 'dataset[name]': name }
   )
   print(response)
   # json = response.json()
   # print(json)
   # return json["html_url"]
submit_to_dolos('student_P.zip','dolos\\student_P.zip')