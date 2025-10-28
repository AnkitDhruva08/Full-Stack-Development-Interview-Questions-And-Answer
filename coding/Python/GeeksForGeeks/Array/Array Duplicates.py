# Given an array arr[] of size n, containing elements from the range 1 to n, 
# and each element appears at most twice, return an array of all the integers that appears twice.

# Note: You can return the elements in any order but the driver code will print them in sorted order.

# Input: arr[] = [2, 3, 1, 2, 3]
# Output: [2, 3] 
# Explanation: 2 and 3 occur more than once in the given array.
# Input: arr[] = [3, 1, 2] 
# Output: []
# Explanation: There is no repeating element in the array, so the output is empty.

arr =list(map(int,input('Enter list of values ::: ').split(',')))
result_map = {}

for i in arr:
    if i in result_map:
        result_map[i] += 1 
    else:
        result_map[i] = 1

print('result_map ==<<<>>', result_map)
result_arr = []
for k, v in result_map.items():
    if v >= 2:
        result_arr.append(k)

print('result_arr ==<<<>>', result_arr)
