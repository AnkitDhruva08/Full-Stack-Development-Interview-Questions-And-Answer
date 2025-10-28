# Given an array arr[], find the first repeating element.
# The element should occur more than once and the index of its first occurrence should be the smallest.

# Note:- The position you return should be according to 1-based indexing. 

# Input: arr[] = [1, 5, 3, 4, 3, 5, 6]
# Output: 2
# Explanation: 5 appears twice and its first appearance is at index 2 which is less than 3 whose first the occurring index is 3.
# Input: arr[] = [1, 2, 3, 4]
# Output: -1
# Explanation: All elements appear only once so answer is -1.

def firstRepeated( arr):
    # Dictionary to count frequency
    freq = {}
    
    # Count occurrences
    for num in arr:
        freq[num] = freq.get(num, 0) + 1

    
    # Find first repeating element by original order
    for idx, num in enumerate(arr):
        if freq[num] > 1:
            return idx + 1   # 1-based index
    
    # If no repeating element
    return -1


arr = list(map(int,input('Enter a list of values : ').split(' ')))
print('firstRepeated ==<<<>>', firstRepeated(arr))