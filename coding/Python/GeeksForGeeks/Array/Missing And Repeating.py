# Given an unsorted array arr[] of size n, containing elements from the range 1 to n,
# it is known that one number in this range is missing,
# and another number occurs twice in the array, find both the duplicate number and the missing number.

# Input: arr[] = [2, 2]
# Output: [2, 1]
# Explanation: Repeating number is 2 and the missing number is 1.
# Input: arr[] = [1, 3, 3] 
# Output: [3, 2]
# Explanation: Repeating number is 3 and the missing number is 2.
# Input: arr[] = [4, 3, 6, 2, 1, 1]
# Output: [1, 5]
# Explanation: Repeating number is 1 and the missing number is 5.

arr = list(map(int,input('Enter a list of values : ').split(',')))
result_arr = []
set_arr = list(set(arr))
print('set_arr ==<<>>', set_arr)
map_list = {}
for i in arr:
    if i in map_list:
        map_list[i] += 1
    else:
        map_list[i] = 1 


for k, v in map_list.items():
    if v > 1:
        result_arr.append(k)


l=len(set_arr)+1
print('l ==<<>>', l)
total=l*(l+1)//2
print('total =<<<>>', total)
result =  total-sum(set_arr)
print('result ==<<>', result)
result_arr.append(result)
print('result_arr =<<<>>', result_arr)