"""

Given an array arr[] denoting heights of n towers and a positive integer k.

For each tower, you must perform exactly one of the following operations exactly once.

Increase the height of the tower by k
Decrease the height of the tower by k
Find out the minimum possible difference between the height of the shortest and tallest towers after you have modified each tower.

You can find a slight modification of the problem here.
Note: It is compulsory to increase or decrease the height by k for each tower. After the operation, the resultant array should not contain any negative integers.

Examples :

Input: k = 2, arr[] = [1, 5, 8, 10]
Output: 5
Explanation: The array can be modified as [1+k, 5-k, 8-k, 10-k] = [3, 3, 6, 8]. The difference between the largest and the smallest is 8-3 = 5.
Input: k = 3, arr[] = [3, 9, 12, 16, 20]
Output: 11
Explanation: The array can be modified as [3+k, 9+k, 12-k, 16-k, 20-k] = [6, 12, 9, 13, 17]. The difference between the largest and the smallest is 17-6 = 11. 
"""

arr = list(map(int,input("Enter the array elements: ").split(',')))
k = int(input("Enter the value of k: "))
n = len(arr)
arr.sort()
ans = arr[n-1] - arr[0]
small = arr[0] + k
big = arr[n-1] - k
if small > big:
    small, big = big, small
for i in range(1, n-1):
    subtract = arr[i] - k
    add = arr[i] + k
    if subtract >= small or add <= big:
        continue
    if big - subtract <= add - small:
        small = subtract
    else:
        big = add
print(min(ans, big - small))