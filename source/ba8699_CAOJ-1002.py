# 讀取輸入
N = int(input())  # 讀取第一行，N 代表數字的個數
numbers = list(map(int, input().split()))  # 讀取第二行並將數字轉換為整數列表

# 排序
sorted_numbers = sorted(numbers)

# 輸出排序後的結果
print(" ".join(map(str, sorted_numbers)))
