"""
35. Search Insert Position
Easy
Topics
premium lock icon
Companies
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

 

Example 1:

Input: nums = [1,3,5,6], target = 5
Output: 2
Example 2:

Input: nums = [1,3,5,6], target = 2
Output: 1
Example 3:

Input: nums = [1,3,5,6], target = 7
Output: 4
 

Constraints:

1 <= nums.length <= 104
-104 <= nums[i] <= 104
nums contains distinct values sorted in ascending order.
-104 <= target <= 104
"""

nums = list(map(int,input("Enter list of values ::: ").split(',')))
target = int(input('Enter target value ::  '))

result_index = 0

for i in range(len(nums)):
    flag = True
    if target == nums[i]:
        result_index = i
        flag = False
        break

    elif target < nums[i]:
        result_index = i - 1
        nums.insert(result_index, target)
        flag = False
        break

    elif target > nums[i]:
        result_index = i + 1
        nums.insert(result_index, target)
        flag = False
        break


print('nums ==<<>>', nums)
print('result_index ==<<<>>', result_index)
