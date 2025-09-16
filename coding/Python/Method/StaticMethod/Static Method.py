"""
3️⃣ Static Method

Declared with @staticmethod.

Does not take self or cls.

Cannot access instance or class variables.

Behaves like a normal function, but logically grouped inside the class.
"""


class MathUtils:
    @staticmethod
    def add(x, y):
        return x + y

print(MathUtils.add(5, 10))  # 15


"""
📌 Definition: A method that does not depend on instance or class data, and works like a regular function placed inside a class for logical grouping.
"""