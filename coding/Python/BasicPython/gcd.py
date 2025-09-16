def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    if a == b:
        return a
    if a > b:
        return gcd(a - b, b)
    else:
        return gcd(b - a, a)

a = int(input('Enter values of a :: '))
b = int(input('Enter values of b :: '))
print(gcd(a, b))
