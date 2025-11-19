# Minimum times A has to be repeated such that B is a substring of it
# Given two strings A and B. Find minimum number of times A has to be repeated such that B is a Substring of it.
# If B can never be a substring then return -1.

# Input:
# A = "abcd"
# B = "cdabcdab"
# Output:
# 3
# Explanation:
# Repeating A three times (“abcdabcdabcd”),
# B is a substring of it. B is not a substring
# of A when it is repeated less than 3 times.
# Example 2:
# Input:
# A = "ab"
# B = "cab"
# Output :
# -1
# Explanation:
# No matter how many times we repeat A, we can't
# get a string such that B is a substring of it.



def minRepeats(A, B):
    n = len(b)// len(a)
    print('n ==<<>>', n)

    # Minimum number of Possible Repeatition if length B is exact multiple of length of A 
    if B in A * n:
        return n  

    # Minimum number of Possible Repeatition if length B is not exact multiple of length of A 
    if B in A * (n+1):
        return n + 1 

    # Maximum number of Possible Repeatition if length B is not exact multiple of length of A 
    if B in A * (n+2):
        return n + 2 

    return -1


# main program
A = input('Enter String A : ')
B = input('Enter String B : ')
print('Minimum Repeats Required ::: ', minRepeats(A, B))