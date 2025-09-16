class Person:
    def __init__(self, name):
        self.name = name


class Empoloyee(Person):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary 


e = Empoloyee("Ankit", 5000)
print(e.name, e.salary)