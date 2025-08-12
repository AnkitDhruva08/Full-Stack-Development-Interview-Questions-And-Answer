# 15. Write a code to replace each element in an array by its rank in the array
# This problem asks to replace each element in an array by its rank in the array.

# The rank of an element is its position in the sorted array (with ties assigned the same rank).
# Example for array [40, 10, 20, 30]:
# After replacing each element by its rank, the array will be [4, 1, 2, 3] (after sorting, the elements are [10, 20, 30, 40], so ranks are [1, 2, 3, 4]).


arr = list(map(int, input('Enter number of values ::: ').split(',')))

sorted_arr = sorted(arr)

rank_map = {}
rank = 1
for num in sorted_arr:
    if num not in rank_map:  
        rank_map[num] = rank
        rank += 1

for i in range(len(arr)):
    arr[i] = rank_map[arr[i]]

print('Ranked array ==<<<>>>', arr)
