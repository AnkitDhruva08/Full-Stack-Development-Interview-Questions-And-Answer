n = int(input('Enter range ::::  '))

a = int(input('Enter Values of a ::: '))
b = int(input('Enter Values of b ::: '))
series = [a, b]

for i in range(2, n +1):
    next_term = a + b 
    a = b 
    b = next_term
    series.append(b)


print('series ==<<<>>', series)

