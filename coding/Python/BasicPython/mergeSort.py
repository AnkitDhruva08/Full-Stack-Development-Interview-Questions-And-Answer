# 10. How is the merge sort algorithm implemented?
# Merge Sort is a divide-and-conquer algorithm that splits the list into smaller sublists, sorts each sublist, and then merges the sorted sublists.

# The process continues recursively until the entire list is sorted.
# Example for list [5, 3, 8, 4, 2]:
# After sorting, the list will be [2, 3, 4, 5, 8].


arr = list(map(int, input('Enter number of values ::: ').split(',')))

# Step 1: Break the array into sublists of length 1 
sublists = [[x] for x in arr]

# Step 2: Keep merging sublists until only one sorted list remains
while len(sublists) > 1:
    merged_sublists = []
    
    # Take pairs of sublists and merge them
    for i in range(0, len(sublists), 2):
        if i + 1 < len(sublists):  
            left = sublists[i]
            right = sublists[i + 1]
            merged = []
            li = 0
            ri = 0
            
            # Merge two sorted lists
            while li < len(left) and ri < len(right):
                if left[li] <= right[ri]:
                    merged.append(left[li])
                    li += 1
                else:
                    merged.append(right[ri])
                    ri += 1
            
            # Add any remaining elements
            while li < len(left):
                merged.append(left[li])
                li += 1
            
            while ri < len(right):
                merged.append(right[ri])
                ri += 1
            
            merged_sublists.append(merged)
        else:
            # Odd list out, just carry it forward
            merged_sublists.append(sublists[i])
    
    # Update sublists with newly merged ones
    sublists = merged_sublists

# Step 3: Final sorted array
sorted_arr = sublists[0]
print('Sorted ==<<<>>>', sorted_arr)
