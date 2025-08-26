"""
🔹 What is Selection Sort?

Selection Sort is a simple sorting algorithm that repeatedly selects the smallest (or largest) element from the unsorted part of the array and places it in the correct position.

Think of it like arranging playing cards: you pick the smallest card and put it in front, then repeat for the rest.

🔹 How Selection Sort Works

Steps for an array [64, 25, 12, 22, 11]:

Find the smallest element → 11 → swap with first → [11, 25, 12, 22, 64]

Next smallest from remaining → 12 → swap with second → [11, 12, 25, 22, 64]

Next smallest → 22 → swap with third → [11, 12, 22, 25, 64]

Next smallest → 25 → already in place → [11, 12, 22, 25, 64]
✅ Sorted!

🔹 Algorithm

Start from index i = 0

Find the minimum element in the unsorted portion (i+1 to n-1)

Swap it with element at index i

Repeat until all elements are sorted
"""


arr = list(map(int,input("Enter Arrays Values ::: ").split(',')))

for i in range(len(arr)):
    min_idx = i 
    for j in range(i + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
        
    arr[i] , arr[min_idx] = arr[min_idx], arr[i]



print('arr ==<<<>>', arr)