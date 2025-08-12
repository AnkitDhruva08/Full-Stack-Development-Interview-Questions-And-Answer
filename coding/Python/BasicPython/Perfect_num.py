num = int(input('Enter a Number ::: '))
temp = num
l = []
per = 0

for i in range(1, temp // 2 + 1):
    if( temp % i == 0):
        per += i 
        l.append(i)



print('l ==<<<>>', sum(l))
print('per ==<<<>>', per)