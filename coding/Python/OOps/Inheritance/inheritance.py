class Employee:
    def __init__(self, name, salary):
        self.name = name         # Public
        self._salary = salary    # Protected
        self.__bonus = 1000      # Private

    # Getter for private variable
    def get_bonus(self):
        return self.__bonus

    # Setter for private variable
    def set_bonus(self, amount):
        if amount > 0:
            self.__bonus = amount
        else:
            print("Invalid bonus amount")


# Usage
emp = Employee("Alice", 50000)

print(emp.name)          # Public → Accessible
print(emp._salary)       # Protected → Accessible but should be used with caution
# print(emp.__bonus)     # Private → AttributeError

print(emp.get_bonus())   # Access private variable via getter
emp.set_bonus(2000)      # Modify private variable via setter
print(emp.get_bonus())



"""
✅ Key Points:

Encapsulation hides data and allows controlled access.

Private variables → __var (name mangling)

Protected variables → _var (convention, not enforced)

Use getter and setter methods to access or modify private data.
"""