"""
✅ Types of Methods in Python Classes
1️⃣ Instance Method (default method)

Defined with self as the first parameter.

Can access and modify instance variables and class variables.

Most commonly used type of method.
"""



class Person:
    def __init__(self, name):
        self.name = name  # instance variable
    
    def greet(self):  # instance method
        return f"Hello, I am {self.name}"

p = Person("Ankit")
print(p.greet())  # Hello, I am Ankit


"""
📌 Definition: A method that works with object/instance data and always takes self as its first argument.
"""