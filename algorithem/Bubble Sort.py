"""
What is Bubble Sort?

Bubble Sort is one of the simplest sorting algorithms.
It works by repeatedly swapping adjacent elements if they are in the wrong order.

Imagine bubbles rising in water: the largest bubble slowly moves to the top → hence the name Bubble Sort.

🔹 How Bubble Sort Works

Compare the first two elements.

If the first > second, swap them.

Move to the next pair and repeat.

After one full pass, the largest element is at the end.

Repeat the process for remaining elements until sorted.
"""


arr = list(map(int,input("Enter array :::").split(',')))

for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        if arr[i] > arr[j]:
            arr[i], arr[j] = arr[j], arr[i]


print('arr <<<>>', arr)