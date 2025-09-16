"""
🧠 Coupling

Definition:
Coupling refers to how much one module/class depends on another.

High coupling → Modules are tightly connected; changes in one module may break the other.

Low coupling → Modules are independent; changes in one module do not affect others.
"""

# Example of Tightly Coupled Code:
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()  # Car is tightly coupled to Engine

    def start_car(self):
        self.engine.start()

car = Car()
car.start_car()



"""
🧠 Decoupling

Definition:
Decoupling is the process of reducing dependencies between modules so that they can operate independently.

This makes the code more maintainable, flexible, and reusable.
"""


# Example of Decoupled Code (Using Dependency Injection):
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self, engine):
        self.engine = engine  # Inject dependency

    def start_car(self):
        self.engine.start()

engine = Engine()
print('Assigning engine to car')
car = Car(engine)  # Engine passed in
car.start_car()