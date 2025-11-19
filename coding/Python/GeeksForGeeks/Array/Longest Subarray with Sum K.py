# Given an array arr[] containing integers and an integer k, 
# your task is to find the length of the longest subarray where the sum of its elements is equal to the given value k.
# If there is no subarray with sum equal to k, return 0.

# Input: arr[] = [10, 5, 2, 7, 1, -10], k = 15
# Output: 6
# Explanation: Subarrays with sum = 15 are [5, 2, 7, 1], [10, 5] and [10, 5, 2, 7, 1, -10]. The length of the longest subarray with a sum of 15 is 6.
# Input: arr[] = [-5, 8, -14, 2, 4, 12], k = -5
# Output: 5
# Explanation: Only subarray with sum = -5 is [-5, 8, -14, 2, 4] of length 5.
# Input: arr[] = [10, -10, 20, 30], k = 5
# Output: 0
# Explanation: No subarray with sum = 5 is present in arr[].

def longestSubarray(arr, k):
    prefix_sum = 0
    sum_index_map = {}
    max_len = 0
    
    for i in range(len(arr)):
        prefix_sum += arr[i]
    
        # Case 1: entire subarray from 0 to i has sum = k
        if prefix_sum == k:
            max_len = i + 1
    
        # Case 2: check if prefix_sum - k was seen before
        if (prefix_sum - k) in sum_index_map:
            max_len = max(max_len, i - sum_index_map[prefix_sum - k])
    
            # Store prefix_sum if not already stored
        if prefix_sum not in sum_index_map:
            sum_index_map[prefix_sum] = i
    
    return max_len


# main program
arr = list(map(int,input('Enter list of values : ').split(',')))
k = int(input('Enter values of k : '))
print('Output <<<> ::: ', longestSubarray(arr, k))