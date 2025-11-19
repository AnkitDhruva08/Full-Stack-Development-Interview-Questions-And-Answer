# Given an array arr[]. The task is to find the largest element and return it.
# Input: arr[] = [1, 8, 7, 56, 90]
# Output: 90
# Explanation: The largest element of the given array is 90.
# Input: arr[] = [5, 5, 5, 5]
# Output: 5
# Explanation: The largest element of the given array is 5.
# Input: arr[] = [10]
# Output: 10
# Explanation: There is only one element which is the largest.

def largest( arr):

    return max(arr) 


# main program
arr = list(map(int,input('Enter list of values : ').split(',')))
print('Output <<<> ::: ', largest(arr))