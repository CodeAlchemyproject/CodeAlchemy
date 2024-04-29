import os

# 更改当前工作目录到 dolos 文件夹下
os.chdir('dolos')

# 运行命令
os.system('wsl dolos run -f web student_P.zip --host 192.168.0.1')