# Given an array arr[]. Your task is to find the minimum and maximum elements in the array.
# Input: arr[] = [1, 4, 3, -5, -4, 8, 6]
# Output: [-5, 8]
# Explanation: minimum and maximum elements of array are -5 and 8.
# Input: arr[] = [12, 3, 15, 7, 9]
# Output: [3, 15]
# Explanation: minimum and maximum element of array are 3 and 15.

arr = list(map(int,input("Enter Array Values : ").split(',')))
print('arr ==<<<>>', arr)

result_arr = []
max_val = arr[0]
min_val = arr[0]

for i in arr:
    if max_val < i:
        max_val = i 
    if min_val > i:
        min_val = i 

result_arr = [min_val, max_val]
print('result_arr ==<<<<>>', result_arr)

for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j] , arr[i]

result_arr = [arr[0], arr[-1]]




