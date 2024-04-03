import re

# 要處理的字串
html_string = '<div class="problembox" id="problem_content"><p>學習所有程式語言的第一個練習題 <br/>請寫一個程式，可以讀入指定的字串，並且輸出指定的字串。</p> <p>比如：輸入字串 "world", 則請輸出 "hello, world"</p> </div>'

# 使用正規表達式將第一個<p>前面的所有文字和最後一個</p>後面的文字去除
cleaned_string = re.sub(r'^.*?<p>', '<p>', html_string, 1)
cleaned_string = re.sub(r'</p>.*?$', '</p>', cleaned_string, 1)

print(cleaned_string)
