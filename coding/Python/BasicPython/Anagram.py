# 5. Write code to Check if two strings are Anagram or not
# Two strings are called anagrams if they contain the same characters in the same frequencies, but possibly in different orders.

# This code checks whether two given strings are anagrams of each other.
# Example: Are listen and silent anagrams?
# Sort both:
# “listen” → “eilnst”

# “silent” → “eilnst”
# Both are the same, so “listen” and “silent” are anagrams.



s1 = input("enter s1 string ::: ")
s2 = input("enter s2 string ::: ")
l1 = []
l2 = []

if (len(s1) == len(s2)):
    for i in range(len(s1)):
        l1.append(ord(s1[i]))
        l2.append(ord(s2[i]))



print("sum ==<<>>", sum(l1))
print("sum ==<<>>", sum(l2))

