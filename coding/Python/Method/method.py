class Person:
    # Class variable
    species = "Human"

    # 1️⃣ Special Method (constructor)
    def __init__(self, name, age):
        self.name = name      # instance variable
        self.age = age        # instance variable

    # 2️⃣ Instance Method
    def greet(self):
        return f"Hi, I am {self.name}, {self.age} years old."

    # 3️⃣ Class Method
    @classmethod
    def describe_species(cls):
        return f"All persons are of species: {cls.species}"

    # 4️⃣ Class Method (Factory Method)
    @classmethod
    def from_string(cls, data_str):
        name, age = data_str.split("-")
        return cls(name, int(age))

    # 5️⃣ Static Method
    @staticmethod
    def is_adult(age):
        return age >= 18

    # 6️⃣ Special Method (string representation)
    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"


# -------------------------
# 🔥 Usage of All Methods
# -------------------------

# Creating object using normal constructor
p1 = Person("Ankit", 27)

# Instance Method
print(p1.greet())  # Hi, I am Ankit, 27 years old.

# Class Method
print(Person.describe_species())  # All persons are of species: Human

# Class Method as Factory
p2 = Person.from_string("Rahul-30")
print(p2.greet())  # Hi, I am Rahul, 30 years old.

# Static Method
print(Person.is_adult(15))  # False
print(Person.is_adult(20))  # True

# Special Method (__str__)
print(p1)  # Person(name=Ankit, age=27)
print(p2)  # Person(name=Rahul, age=30)
