num = int(input('Enter A Number :::  '))

temp = num 
reverse = 0

while temp != 0:
    r = temp % 10 
    print('r ==<<<>>', r)
    reverse = reverse * 10 + r 
    print('reverse ==<<<>>', reverse)
    temp = temp // 10

print('reverse ==<<<>>', reverse)
