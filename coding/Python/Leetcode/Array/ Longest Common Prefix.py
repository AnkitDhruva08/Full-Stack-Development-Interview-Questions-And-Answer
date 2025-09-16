"""

14. Longest Common Prefix
Solved
Easy
Topics
premium lock icon
Companies
Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

 

Example 1:

Input: strs = ["flower","flow","flight"]
Output: "fl"
Example 2:

Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
 

Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters if it is non-empty.
"""

strs = list(map(str,input("enter string of array :: ").split(',')))
# Remove spaces from each string
strs = [s.replace(" ", "") for s in strs]
min_len = min([len(x) for x in strs])
prefix_str = ''

for i in range(min_len):
    char = strs[0][i]
    flag = True
    for j in strs:
        if j[i] != char:
            flag = False
            break
    if flag:
        prefix_str += char
    else:
        break

print('prefix_str =<<<<>>', prefix_str)



