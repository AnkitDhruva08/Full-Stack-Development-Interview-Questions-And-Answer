"""
🔹 What is Insertion Sort?

Insertion Sort builds the sorted array one item at a time.

It takes one element from the unsorted part and inserts it into the correct position in the sorted part.

Works like sorting playing cards in your hand.

🔹 How Insertion Sort Works

Example: [5, 3, 4, 1, 2]

Start with 2nd element (3) → insert into correct place → [3, 5, 4, 1, 2]

Take next element (4) → insert → [3, 4, 5, 1, 2]

Take next element (1) → insert → [1, 3, 4, 5, 2]

Take next element (2) → insert → [1, 2, 3, 4, 5]
✅ Sorted!

🔹 Algorithm

Iterate from i = 1 to n-1

Store the key = arr[i]

Compare key with elements before it (arr[0..i-1])

Shift larger elements to the right

Insert key in its correct position
"""


arr = list(map(int,input("Enter array :::").split(',')))

for i in range(len(arr)):
    key = arr[i]
    j = i - 1

    # Move elements greater than key to one position ahead
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
        
    arr[j + 1] = key 


print('arr ==<<<>>', arr)
