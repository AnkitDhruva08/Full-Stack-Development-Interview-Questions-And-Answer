# 13. Write a code to replace a substring in a string.
# This problem asks to replace a substring within a string with another substring.

# The goal is to find all occurrences of the target substring and replace them with the desired one.
# Example for string “hello world”:
# Replacing “world” with “Python” results in “hello Python”.



s = input('Enter String :: ')
print('S ==<<>>', s)

l = list((s).split(' '))

l[1] = 'Python'

print('l ==<<<>>', l)

print(' '.join(l))