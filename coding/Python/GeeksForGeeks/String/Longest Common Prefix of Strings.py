# Given an array of strings arr[]. Return the longest common prefix among each and every strings present in the array.
# If there's no prefix common in all the strings, return "".

# Input: arr[] = ["geeksforgeeks", "geeks", "geek", "geezer"]
# Output: "gee"
# Explanation: "gee" is the longest common prefix in all the given strings.
# Input: arr[] = ["hello", "world"]
# Output: ""
# Explanation: There's no common prefix in the given strings.

def longestCommonPrefix(arr):
    if not arr:
        return ""
    
    prefix = arr[0]
    
    for string in arr[1:]:
        while string.find(prefix) != 0:
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix 

# main program
arr = input('Enter List of strings : ').split(',')
print('Longest Common Prefix ::: ', longestCommonPrefix(arr))