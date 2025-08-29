class Employee:
    def __init__(self, name, salary):
        self.name = name 
        self.salary = salary 

e = Employee("Ankit", 5000)   # __init__ called automatically
print(e.name, e.salary)
