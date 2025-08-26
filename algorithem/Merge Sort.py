"""
🔹 Merge Sort

Merge Sort is a Divide and Conquer algorithm.
It divides the array into smaller parts, sorts them, and then merges them back together.

🔹 How Merge Sort Works

Divide → Split the array into two halves

Conquer → Recursively sort both halves

Example: [38, 27, 43, 3, 9, 82, 10]

Split → [38, 27, 43, 3] and [9, 82, 10]

Keep splitting until single elements → [38] [27] [43] [3] [9] [82] [10]

Merge sorted pairs → [27, 38] [3, 43] [9, 82] [10]

Merge again → [3, 27, 38, 43] and [9, 10, 82]

Final merge → [3, 9, 10, 27, 38, 43, 82] ✅
"""




def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Find midpoint
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursive sorting
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge step
        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy remaining elements
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

# Example
nums = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(nums))  # Output: [3, 9, 10, 27, 38, 43, 82]
