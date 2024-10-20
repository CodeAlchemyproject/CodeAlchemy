# 氣泡排序演算法
def bubble_sort(arr):
    n = len(arr)
    # 逐一比較相鄰的元素，直到所有元素排序完成
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # 交換元素
                arr[j], arr[j+1] = arr[j+1], arr[j]

# 讀取輸入
N = int(input())  # 讀取第一行，N 代表數字的個數
numbers = list(map(int, input().split()))  # 讀取第二行並將數字轉換為整數列表

# 排序
bubble_sort(numbers)

# 輸出排序後的結果
print(" ".join(map(str, numbers)))
