import requests # pip install requests

def submit_to_dolos(name, zipfile_path):
   """
   Submit a ZIP-file to the Dolos API for plagiarism detection
   and return the URL where the resulting HTML report can be found.
   """
   response = requests.post(
      'http://localhost:3000/reports',
      files = { 'dataset[zipfile]': open(zipfile_path, 'rb') },
      data = { 'dataset[name]': name }
   )
   print(response)
   json = response.json()
   return json["html_url"]
print(submit_to_dolos('dolos','dolos\student_P.zip'))