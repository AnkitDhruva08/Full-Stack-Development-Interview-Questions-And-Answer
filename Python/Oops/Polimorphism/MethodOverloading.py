class Calculator:
    def add(self, a = 0, b = 0, c = 0):

        return a + b + c 
    


c = Calculator()

print(c.add(10))
print(c.add(10, 20))
print(c.add(10, 20, 30))
        


class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(1, 2))        # 3
print(calc.add(1, 2, 3, 4))  # 10