"""
4. Median of Two Sorted Arrays
Solved
Hard
Topics
premium lock icon
Companies
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

 

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
 

Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-106 <= nums1[i], nums2[i] <= 106
"""

nums1 = list(map(int,input("Enter first list elements ::: ").split(',')))
nums2 = list(map(int,input("Enter second list elements ::: ").split(',')))
nums3 = nums1 + nums2
print('nums3 ==<<<>>', nums3)

def merg_sort(nums3):
# using mersort approach
    if len(nums3) > 1:
        mid = len(nums3) // 2
        left_half = nums3[:mid]
        right_half = nums3[mid:]

        # recusrsive for sorting the array
        merg_sort(left_half)
        merg_sort(right_half)

        # Merge step
        i = j = k = 0

        while i < len(left_half)  and j < len(right_half):
            if left_half[i] < right_half[j]:
                nums3[k] = left_half[i]

                i += 1
            else:
                nums3[k] = right_half[j]

                j += 1 
            k += 1

        # Copy remaining elements

        while i < len(left_half):
            nums3[k] = left_half[i]

            i += 1
            k += 1 

        while j < len(right_half):
            nums3[k] = right_half[j]

            j += 1
            k += 1 

        return nums3

print(merg_sort(nums3))
median = 0
# Median # Odd length
if len(nums3) % 2 == 1:
    median = nums3[(len(nums3)) // 2]

# Even length

else:
    mid1 = nums3[len(nums3) // 2 - 1]
    mid2 = nums3[len(nums3) // 2]
    median = (mid1 + mid2) / 2

print('median ==<<<>>', median)




