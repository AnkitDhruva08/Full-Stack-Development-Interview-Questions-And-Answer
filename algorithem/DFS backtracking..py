"""
🔎 What is DFS Backtracking?

DFS (Depth First Search):
Explore as deep as possible along one branch before backtracking (returning to try another branch).
It’s like following one path in a maze until you hit a dead end, then going back and trying another path.

Backtracking:
A technique where we build a solution step by step, and undo (backtrack) if we realize the current path doesn’t lead to a valid solution.
It systematically explores all possibilities but avoids unnecessary exploration by pruning invalid states.

🛠️ General Steps of DFS Backtracking

Choose: Pick an option (e.g., pick a number, move in a direction, choose a letter).

Explore: Recurse (go deeper) with that choice added to the current solution.

Un-choose (Backtrack): Remove the choice before trying the next option.

This pattern is repeated until all valid solutions are found.

⚡ Example 1: Generate All Binary Strings of Length 3

We want all possible strings of 0 and 1 of length 3.

Algorithm (DFS Backtracking):

Start with an empty string.

At each step: choose 0 or 1.

Recurse until length = 3.

If length = 3 → save result.

Backtrack to try other choices.
"""

"""
[]
 ├─ [0]
 │   ├─ [0,0]
 │   │   ├─ [0,0,0] ✅
 │   │   └─ [0,0,1] ✅
 │   └─ [0,1]
 │       ├─ [0,1,0] ✅
 │       └─ [0,1,1] ✅
 └─ [1]
     ├─ [1,0]
     │   ├─ [1,0,0] ✅
     │   └─ [1,0,1] ✅
     └─ [1,1]
         ├─ [1,1,0] ✅
         └─ [1,1,1] ✅

"""


"""
Example 2: Rat in a Maze

A rat starts at the top-left corner of a grid.

It can move down or right until it reaches the bottom-right corner.

DFS Backtracking explores all paths step by step.

If it hits a wall (invalid), it backtracks and tries another path.

✨ Key Points to Remember

DFS Backtracking = DFS + undoing choices.

Always follow the Choose → Explore → Backtrack pattern.

Useful for:

Generating subsets/permutations.

Solving mazes.

N-Queens, Sudoku.

Word search problems.
"""


results = []
nums = [1, 2, 3]

def backtrack(path, used):
    if len(path) == len(nums):   # base case     
        results.append(path[:])
        return
    print('results :::', results)
    for i in range(len(nums)):
        if used[i]:  
            continue
        path.append(nums[i])   # choose
        used[i] = True
        backtrack(path, used)  # explore
        path.pop()             # un-choose
        used[i] = False

backtrack([], [False] * len(nums))
print(results)
