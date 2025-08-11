# Input: mat[][] = [[1, 2, -1, -4, -20], [-8, -3, 4, 2, 1], [3, 8, 10, 1, 3], [-4, -1, 1, 7, -6]]
# Output: 29
# Explanation: The matrix is as follows and the green rectangle denotes the maximum sum rectangle which is equal to 29.



arr =  [[1, 2, -1, -4, -20], [-8, -3, 4, 2, 1], [3, 8, 10, 1, 3], [-4, -1, 1, 7, -6]]

def maximumSumRectangle(arr):
    if not arr or not arr[0]:
        return 0

    rows, cols = len(arr), len(arr[0])
    max_sum = float('-inf')

    for left in range(cols):
        temp = [0] * rows
        for right in range(left, cols):
            for i in range(rows):
                temp[i] += arr[i][right]

            current_sum = 0
            current_max = float('-inf')
            for value in temp:
                current_sum += value
                if current_sum > current_max:
                    current_max = current_sum
                if current_sum < 0:
                    current_sum = 0

            max_sum = max(max_sum, current_max)

    return max_sum
print(maximumSumRectangle(arr)) 