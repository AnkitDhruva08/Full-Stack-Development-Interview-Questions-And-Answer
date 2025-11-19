🧠 Introduction to Algorithm

An algorithm is a step-by-step procedure or a set of well-defined instructions designed to perform a specific task or solve a particular problem.

In simple terms, an algorithm tells a computer exactly what steps to take, in what order, to achieve a desired output from a given input.

Algorithms are the foundation of computer programming and problem-solving — every program or software you use is built using one or more algorithms.


---------------------------------------------------------------------------------------------------------------------------------------------------

🧩 Analysis of Algorithms

When we design an algorithm, we need to know how efficient it is — in terms of time (how long it takes) and space (how much memory it uses).
To measure that, we perform Algorithm Analysis, which can be done in two ways:

1️⃣ Priori Analysis (Theoretical Analysis)
📘 Definition:

Priori analysis means analyzing an algorithm theoretically, before implementing it in any programming language.

💡 Explanation:

It is based on logical reasoning and mathematical estimation.

We don’t run the program; instead, we study the algorithm’s code or pseudocode and calculate its time complexity and space complexity.

For example, we analyze how many operations an algorithm performs for input size ‘n’ — like O(n), O(n²), etc.

🧠 Example:

If an algorithm has a loop that runs ‘n’ times, we can say its time complexity = O(n) without actually running it.

2️⃣ Posteriori Analysis (Empirical Analysis)
📘 Definition:

Posteriori analysis means analyzing an algorithm after implementing and executing it on a computer.

💡 Explanation:

It is based on real-world observation and testing.

We run the program with different input sizes and measure the actual running time and memory usage.

It helps to check how the algorithm performs in practical conditions (considering CPU speed, compiler, system load, etc.).

🧠 Example:

Running a sorting algorithm on your computer and recording how long it takes for 1,000, 10,000, and 100,000 elements — that’s posteriori analysis.


----------------------------------------------------------------------------------------------------------------------------------------------------------
✳️ Characteristics of an Algorithm

Input:
An algorithm should have zero or more inputs that are provided before the algorithm starts.
These inputs supply the data that the algorithm will process.

Output:
Every algorithm must produce at least one output — a result or solution that represents the outcome of the processing.

Definiteness (Clarity):
Each step of the algorithm must be clearly and unambiguously defined.
There should be no confusion or vague instructions — every instruction must be precise and well-defined.

Finiteness:
An algorithm must always terminate after a finite number of steps.
It should not run indefinitely; it should reach a conclusion within a definite time.

Effectiveness:
Each step of the algorithm should be simple, basic, and executable.
It must be written in a way that is readable, understandable, and practically implementable using available resources.
----------------------------------------------------------------------------------------------------------------------------------------------------------

✍️ How to Write an Algorithm

An algorithm is written in simple, step-by-step English-like statements or pseudocode that describe how to solve a problem.

When writing an algorithm:

Focus on logic and sequence of steps, not on programming syntax.

It should be clear, simple, and language-independent.

Data types are not required — you just mention the variables and their operations.

Each step should be numbered or clearly separated for readability.

Use keywords like Start, Stop, Input, Output, Compute, Display, etc.

Algorithm: Swap Two Numbers
Step 1: Start
Step 2: Input a, b
Step 3: temp ← a
Step 4: a ← b
Step 5: b ← temp
Step 6: Display a, b
Step 7: Stop



How To Analyze an algorithem 

1. Time 
2. space -- how much memory space it will take
3. n/w - how much is going to transfer
4. power 
5. cpu registered









------------------------------------
🧠 1. Searching Algorithms

Used to find an element in a data structure (like array or list).

Linear Search

Binary Search

Jump Search

Interpolation Search

Exponential Search

Fibonacci Search

⚙️ 2. Sorting Algorithms

Used to arrange data in a specific order (ascending or descending).

Bubble Sort

Selection Sort

Insertion Sort

Merge Sort

Quick Sort

Heap Sort

Counting Sort

Radix Sort

Bucket Sort

Shell Sort

🔁 3. Recursion and Divide & Conquer Algorithms

Binary Search (also fits here)

Merge Sort

Quick Sort

Tower of Hanoi

Fibonacci Series

Matrix Multiplication (Strassen’s Algorithm)

🧮 4. Greedy Algorithms

Used for optimization problems — making the best local choice at each step.

Kruskal’s Algorithm (Minimum Spanning Tree)

Prim’s Algorithm (Minimum Spanning Tree)

Dijkstra’s Algorithm (Shortest Path)

Huffman Encoding

Fractional Knapsack Problem

Job Sequencing Problem

🧩 5. Dynamic Programming (DP) Algorithms

Used for problems that can be broken into overlapping subproblems.

Fibonacci Series (DP version)

Longest Common Subsequence (LCS)

Longest Increasing Subsequence (LIS)

0/1 Knapsack Problem

Matrix Chain Multiplication

Coin Change Problem

Bellman-Ford Algorithm

Floyd-Warshall Algorithm

Edit Distance Algorithm

🌐 6. Graph Algorithms

Used to solve problems related to networks and connections.

Depth First Search (DFS)

Breadth First Search (BFS)

Dijkstra’s Algorithm

Bellman-Ford Algorithm

Floyd-Warshall Algorithm

Kruskal’s Algorithm

Prim’s Algorithm

Topological Sorting

Tarjan’s Algorithm (SCC)

Kosaraju’s Algorithm (SCC)

🧱 7. String Algorithms

Used for text and pattern matching.

Naive Pattern Searching

KMP Algorithm (Knuth-Morris-Pratt)

Rabin-Karp Algorithm

Z Algorithm

Boyer-Moore Algorithm

Longest Common Subsequence (LCS)

Longest Palindromic Substring

🧬 8. Backtracking Algorithms

Used for exploring all possibilities — e.g., puzzles, games, combinations.

N-Queens Problem

Sudoku Solver

Rat in a Maze

Hamiltonian Cycle

Graph Coloring

Subset Sum Problem

🧰 9. Divide and Conquer Algorithms

Binary Search

Merge Sort

Quick Sort

Closest Pair of Points

Strassen’s Matrix Multiplication

⚖️ 10. Miscellaneous / Other Important Algorithms

Hashing (for searching and mapping)

Union-Find (Disjoint Set)

Kadane’s Algorithm (Maximum Subarray Sum)

Sliding Window Algorithms

Two Pointer Technique

Fast Fourier Transform (FFT)

Convex Hull (Graham Scan / Jarvis March)
