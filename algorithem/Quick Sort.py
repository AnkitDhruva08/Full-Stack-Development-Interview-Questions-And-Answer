"""
🔹 Quick Sort

Quick Sort is another Divide and Conquer algorithm, but unlike Merge Sort, it sorts in place (doesn’t require extra arrays as much).

🔹 How Quick Sort Works

Pick a pivot element from the array (can be first, last, middle, or random).

Partition the array → put elements smaller than pivot on the left, larger on the right.

Recursively apply Quick Sort to left and right sub-arrays.

The array is sorted once all partitions are done.

Example: [10, 7, 8, 9, 1, 5]

Choose pivot = last element (5)

Partition: [1] [5] [10, 7, 8, 9]

Sort left → [1]

Sort right → [7, 8, 9, 10]

Final array → [1, 5, 7, 8, 9, 10] ✅
"""


def partition(arr, low, high):
    pivot = arr[high]  # choose last element as pivot
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # swap
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)  # partition index
        quick_sort(arr, low, pi - 1)    # sort left side
        quick_sort(arr, pi + 1, high)   # sort right side
    return arr

# Example
nums = [10, 7, 8, 9, 1, 5]
print(quick_sort(nums, 0, len(nums) - 1))  # Output: [1, 5, 7, 8, 9, 10]
