import heapq

class Solution:
    class Node:
        def __init__(self, value, row, col):
            self.value = value
            self.row = row
            self.col = col

        def __lt__(self, other):
            return self.value < other.value

    def findSmallestRange(self, arr):
        k = len(arr)
        n = len(arr[0])

        min_heap = []
        max_val = float('-inf')
        start, end = 0, float('inf')

        # Initialize heap with the first element of each list
        for i in range(k):
            node = self.Node(arr[i][0], i, 0)
            heapq.heappush(min_heap, node)
            max_val = max(max_val, arr[i][0])

        while True:
            curr = heapq.heappop(min_heap)
            min_val = curr.value

            if max_val - min_val < end - start:
                start, end = min_val, max_val

            # If the current list has more elements
            if curr.col + 1 < n:
                next_val = arr[curr.row][curr.col + 1]
                heapq.heappush(min_heap, self.Node(next_val, curr.row, curr.col + 1))
                max_val = max(max_val, next_val)
            else:
                break

        return [start, end]