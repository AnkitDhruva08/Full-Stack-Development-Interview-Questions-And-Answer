"""
Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure.

A heap is a special kind of binary tree where:

In a Max Heap, every parent node ≥ its children.

In a Min Heap, every parent node ≤ its children.

👉 For ascending order, we usually use a Max Heap.

🔹 How Heap Sort Works

Build a max heap from the input array.

Swap the root (largest element) with the last element of the heap.

Reduce the heap size by 1.

Heapify the root again to maintain the max-heap property.

Repeat until the heap size is 1.

Example: [4, 10, 3, 5, 1]

Step 1: Build max heap → [10, 5, 3, 4, 1]

Step 2: Swap root with last → [1, 5, 3, 4, 10]

Step 3: Heapify → [5, 4, 3, 1, 10]

Step 4: Swap root with last unsorted → [1, 3, 4, 5, 10]

Step 5: Continue → [1, 3, 4, 5, 10] ✅ Sorted
"""

def heapify(arr, n, i):
    largest = i      # Initialize largest as root
    left = 2 * i + 1 # left child
    right = 2 * i + 2 # right child

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    # Build max heap
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # swap
        heapify(arr, i, 0)

    return arr

# Example
nums = [4, 10, 3, 5, 1]
print(heap_sort(nums))  # Output: [1, 3, 4, 5, 10]
