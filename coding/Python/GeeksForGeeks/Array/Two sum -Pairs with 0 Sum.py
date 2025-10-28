# Given an integer array arr, return all the unique pairs [arr[i], arr[j]] such that i != j and arr[i] + arr[j] == 0.

# Note: The pairs must be returned in sorted order, the solution array should also be sorted, and the answer must not contain any duplicate pairs.

# Input: arr = [-1, 0, 1, 2, -1, -4]
# Output: [[-1, 1]]
# Explanation: arr[0] + arr[2] = (-1)+ 1 = 0.
# arr[2] + arr[4] = 1 + (-1) = 0.
# The distinct pair are [-1,1].
# Input: arr = [6, 1, 8, 0, 4, -9, -1, -10, -6, -5]
# Output: [[-6, 6],[-1, 1]]
# Explanation: The distinct pairs are [-1, 1] and [-6, 6].

arr = list(map(int,input('Enter list of values : ').split(' ')))
result_arr = []
for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        if(arr[i] + arr[j] == 0 and i != j):
            if(sorted([arr[i] , arr[j]]) not in result_arr):
                result_arr.append(sorted([arr[i] , arr[j]]))


print('result_arr ==<<>>', result_arr)



arr.sort()

i = 0
j = len(arr) - 1

e_set = set()
lst = []

while i < j :
    if arr[i]+arr[j]==0:
        if (arr[i],arr[j]) in e_set:
            continue
        else:
            e_set.add((arr[i],arr[j]))
                    
            lst.append([arr[i],arr[j]])
        i+=1
        j-=1
        
    elif arr[i]+arr[j]>0:
        j-=1
    else:
        i+=1

print(' lst ==<<>>', lst)

