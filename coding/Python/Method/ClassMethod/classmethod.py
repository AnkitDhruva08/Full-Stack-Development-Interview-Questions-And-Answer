"""
2️⃣ Class Method

Declared with @classmethod.

Takes cls (the class itself) as the first parameter.

Can access/modify class-level variables, but not instance variables.

Often used for factory methods (alternate constructors).
"""

class Person:
    species = "Human"
    
    def __init__(self, name):
        self.name = name
    
    @classmethod
    def from_string(cls, name_str):
        return cls(name_str)

p = Person.from_string("Ankit")
print(p.name)      # Ankit
print(p.species)   # Human


"""
📌 Definition: A method bound to the class, not the instance, that takes cls as its first argument and is used for class-level operations.
"""