"""
Given two integer variables a and b, and a boolean variable flag. The task is to check the status and return accordingly.

Return True for the following cases:

Either a or b (not both) is non-negative and the flag is false.
Both a and b are negative and the flag is true.
Otherwise, return False.

Examples: 

Input: a = 1, b = -1, flag = False
Output: True
Explanation: Since a is positive, b is negative, and flag is False, condition 1 holds true, so the function returns True.
Input: a = -182, b = -9121, flag = True
Output: True
Explanation: Since both a and b are negative and flag is True, condition 2 holds true, so the function returns True.
Input: a = 5, b = 3, flag = True
Output: False
Explanation: Neither condition 1 nor condition 2 holds, so the function returns False.

"""

a, b = map(int, input("enter values of a, b ::").split(','))
flag = input('Enter flag values ;: ')

if isinstance(flag, str):
    flag = flag.strip().lower == 'true'


if( a > 0 or b > 0) and not flag :
    print('True')

elif( a < 0 and b < 0  and flag):
    print('True')

else:
    print('False')
























