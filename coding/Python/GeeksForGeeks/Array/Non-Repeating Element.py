# Find the first non-repeating element in a given array arr of integers and if there is not present any non-repeating element then return 0

# Note: The array consists of only positive and negative integers and not zero.


# Input: arr[] = [-1, 2, -1, 3, 2]
# Output: 3
# Explanation: -1 and 2 are repeating whereas 3 is the only number occuring once. Hence, the output is 3. 
# Input: arr[] = [1, 1, 1]
# Output: 0
# Explanation: There is not present any non-repeating element so answer should be 0.
def firstNonRepeating( arr): 
    freq = {}
    result = 0
    for i in arr:
        if i in freq:
            freq[i] += 1

        else:
            freq[i] = 1
    for k, v in freq.items():
        if v == 1:
            result = k 
            break  


    return result 


# main program 
arr = list(map(int,input('Enter list of values : ').split(',')))
print('Output ::: ',firstNonRepeating(arr) )


