# 選擇排序演算法
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # 假設當前索引 i 的值為最小值
        min_idx = i
        # 在未排序的部分中找到最小值
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # 將找到的最小值和當前索引 i 的值交換
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# 讀取輸入
N = int(input())  # 讀取第一行，N 代表數字的個數
numbers = list(map(int, input().split()))  # 讀取第二行並將數字轉換為整數列表

# 排序
selection_sort(numbers)

# 輸出排序後的結果
print(" ".join(map(str, numbers)))
