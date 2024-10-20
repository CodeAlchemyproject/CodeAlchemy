# 讀取第一行的數字，代表有多少個數字需要排序
n = int(input().strip())

# 讀取第二行，並將數字分割成陣列
numbers = list(map(int, input().strip().split()))

# 排序數字
sorted_numbers = sorted(numbers)

# 將排序後的數字輸出，數字之間用空格分隔
print(" ".join(map(str, sorted_numbers)))