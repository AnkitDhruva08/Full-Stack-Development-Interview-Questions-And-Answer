# Given an unsorted array arr[ ] having both negative and positive integers. 
# The task is to place all negative elements at the end of the array without changing the order of positive elements and negative elements.

# Note: Don't return any array, just in-place on the array.

# Input : arr[] = [1, -1, 3, 2, -7, -5, 11, 6 ]
# Output : [1, 3, 2, 11, 6, -1, -7, -5]
# Explanation: By doing operations we separated the integers without changing the order.
# Input : arr[] = [-5, 7, -3, -4, 9, 10, -1, 11]
# Output : [7, 9, 10, 11, -5, -3, -4, -1]

def segregateElements( arr):
    # Your code goes here
    print('arr ==<<<>>>', arr)
    pos = []
    neg = []

    for i in arr:
        if i < 0:
            neg.append(i)
        else:
            pos.append(i)

    index = 0
    p = 0
    g = 0
    while index < len(pos):
        arr[index] = pos[p]

        index += 1 
        p += 1 
    
    while index < len(arr):
        arr[index] = neg[g]
        index += 1 
        g += 1
    
    return arr
    



# main program
arr = list(map(int,input('Enter a list of values : ').split(',')))
print('result ==<<<>>', segregateElements(arr))


def segregateElements( arr):
    # Separate positive and negative elements
    pos = [x for x in arr if x >= 0]
    neg = [x for x in arr if x < 0]

    # Merge them back in place
    arr[:] = pos + neg


print('result ==<<<>>', segregateElements(arr))