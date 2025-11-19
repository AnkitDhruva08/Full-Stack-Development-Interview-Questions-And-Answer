# You are given an array arr[] where no two adjacent elements are same,
# find the index of a peak element. An element is considered to be a peak if it is greater than its adjacent elements (if they exist).

# If there are multiple peak elements, Return index of any one of them.
# The output will be "true" if the index returned by your function is correct; otherwise, it will be "false".

# Note: Consider the element before the first element and the element after the last element to be negative infinity.


# Input: arr = [1, 2, 4, 5, 7, 8, 3]
# Output: true
# Explanation: arr[5] = 8 is a peak element because arr[4] < arr[5] > arr[6].
# Input: arr = [10, 20, 15, 2, 23, 90, 80]
# Output: true
# Explanation: Element 20 at index 1 is a peak since 10 < 20 > 15. Index 5 (value 90) is also a peak, but returning any one peak index is valid.

def peakElement(self, arr):
        n = len(arr)
        if n == 1:
            return 0 
        if arr[0] > arr[1]:
            return 0  
        if arr[n-1] > arr[n-2]:
            return n-1 
        
   
        i = 1
        j = n - 2
        while i <= j:
            mid = (i + j) // 2
            if arr[mid] > arr[mid-1] and arr[mid] > arr[mid+1]:
                return mid  
            elif arr[mid] < arr[mid+1]:
                i = mid + 1  
            else:
                j = mid - 1 
        
        return -1



# main program
arr = list(map(int,input('Enter list of values : ').split(',')))
print('Output <<<> ::: ', peakElement(arr))