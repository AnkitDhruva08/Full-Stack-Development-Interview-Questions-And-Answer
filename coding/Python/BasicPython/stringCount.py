# 7. Write code to Calculate frequency of characters in a string
# This problem asks to calculate the frequency of each character in a given string.

# The goal is to determine how many times each character appears in the string.
# Example for string “hello”:
# ‘h’ appears 1 time
# ‘e’ appears 1 time
# ‘l’ appears 2 times
# ‘o’ appears 1 time


s = input('enter a String ::: ')

d = {}

for i in s:
    if i in d:
        d[i] += 1

    else:
        d[i] = 1


print('d ==<<<>>', d)