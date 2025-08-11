# Check if frequencies can be equal

"""
Given a string s consisting only lowercase alphabetic characters, 
check whether it is possible to remove at most one character such that the 
frequency of each distinct character in the string becomes same.
Return true if it is possible; otherwise, return false.
"""

"""
Input: s = "xyyz"
Output: true 
Explanation: Removing one 'y' will make frequency of each distinct character to be 1.
"""

"""
Input: s = "xyyzz"
Output: true
Explanation: Removing one 'x' will make frequency of each distinct character to be 2.
"""

"""
Input: s = "xxxxyyzz"
Output: false
Explanation: Frequency can not be made same by removing at most one character.
"""

s = input('enter a string ::: ')

dict_str = {} 

for i in s:
    if i in dict_str:
        dict_str[i] += 1
    else:
        dict_str[i] = 1 

print('dict_str ==<<<>>',  dict_str)
