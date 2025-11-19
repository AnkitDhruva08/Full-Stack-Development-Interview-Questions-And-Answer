# Given an array arr[] with non-negative integers representing the height of blocks. If the width of each block is 1,
#  compute how much water can be trapped between the blocks during the rainy season. 

# Input: arr[] = [3, 0, 1, 0, 4, 0 2]
# Output: 10
# Explanation: Total water trapped = 0 + 3 + 2 + 3 + 0 + 2 + 0 = 10 units.

# Input: arr[] = [3, 0, 2, 0, 4]
# Output: 7
# Explanation: Total water trapped = 0 + 3 + 1 + 3 + 0 = 7 units.
# Input: arr[] = [1, 2, 3, 4]
# Output: 0
# Explanation: We cannot trap water as there is no height bound on both sides.
# Input: arr[] = [2, 1, 5, 3, 1, 0, 4]
# Output: 9
# Explanation: Total water trapped = 0 + 1 + 0 + 1 + 3 + 4 + 0 = 9 units.


def maxWater( arr):
    n = len(arr)
    left = 0
    right = n-1
    left_max = 0
    right_max = 0
    water = 0
    while left<right:
        if arr[left]<arr[right]:
            left_max = max(arr[left], left_max)
            water += left_max-arr[left]
            left+=1
        else:
            right_max = max(arr[right], right_max)
            water += right_max-arr[right]
            right-=1
    return water     


# main program 
arr = list(map(int,input('Enter List of of values : ').split(',')))
print('Output ::: ', maxWater(arr))