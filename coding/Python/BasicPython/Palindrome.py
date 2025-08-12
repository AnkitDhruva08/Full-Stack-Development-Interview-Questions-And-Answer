# 6. Write code Check if the given string is Palindrome or not
# A palindrome is a word, phrase, or sequence that reads the same backward as forward, ignoring spaces, punctuation, and capitalization.

# This code checks if a given string is a palindrome.
# Example for a palindrome:
# “madam” — reads the same backward as forward


s = input('Enter a String ::: ')

palindrom = ''

for i in s:
    palindrom = i + palindrom



print('palindrom ==<<<>>', palindrom)
