# # Equal point in a string of brackets
# Given a string str of opening and closing brackets '(' and ')' only. The task is to find an equal point.
# An equal point is an index (0-based) such that the number of closing brackets on the right
# from that point must be equal to the number of opening brackets before that point.

# Input: str = "(())))("
# Output: 4
# Explanation: After index 4, string splits into (()) and ))(. Number of opening brackets in the first part is equal to number of closing brackets in the second part.
# Input : str = "))"
# Output: 2
# Explanation: As after 2nd position i.e. )) and "empty" string will be split into these two parts: So, 
# in this number of opening brackets i.e. 0 in the first part is equal to number of closing brackets in the second part i.e. also 0.


def findIndex(str):
    open_bracket = 0
    closing_bracket = 0 

    for i in str:
        if i == ')':
            closing_bracket+= 1 

    for i in range(len(str)):
        if str[i] == '(':
            open_bracket += 1 
        else:
            closing_bracket -= 1 

        if open_bracket == closing_bracket:
            return i + 1
            
    return 0


# main program
str = input('Enter string of brackets : ')
print('Equal Point Index ::: ', findIndex(str))