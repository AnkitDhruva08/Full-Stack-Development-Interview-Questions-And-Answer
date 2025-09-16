"""
Definition:
Method overriding happens when a child class redefines a method that is already defined in the parent
"""


"""
class.

The child class version of the method will be called instead of the parent’s.

Used in inheritance to change or extend behavior.
"""
class Parent:
    def greet(self):
        return "Hello from Parent"
    

class Child(Parent):
    def greet(self):  # Overriding the greet method
        return "Hello from Child"
    
p = Parent()
c = Child()
print(p.greet())  # Output: Hello from Parent
print(c.greet())  # Output: Hello from Child