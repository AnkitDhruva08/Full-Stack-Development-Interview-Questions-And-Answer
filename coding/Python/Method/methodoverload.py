"""
2️⃣ Method Overloading

Definition:
Method overloading is when multiple methods in the same class have the same name but different parameters.

Python does not support traditional overloading like Java or C++.

But we can achieve it using:

Default arguments

Variable-length arguments (*args, **kwargs)
"""


    


class MathOps1:
    def add(self, a, b, c=0):  # Default argument for c
        return a + b + c
    

m1 = MathOps1()
print(m1.add(2, 3))      
print(m1.add(2, 3, 4))   




class MathOps:
    def add(self, a, b, c=0, **kwargs):
        # Get d from kwargs if passed, default to 0
        d = kwargs.get('d', 0)
        return a + b + c + d

m1 = MathOps()

print(m1.add(2, 3))             # Output: 5 (d=0)
print(m1.add(2, 3, 4))          # Output: 9 (d=0)
print(m1.add(2, 3, d=2))        # Output: 7
print(m1.add(2, 3, 4, d=2))     # Output: 11
