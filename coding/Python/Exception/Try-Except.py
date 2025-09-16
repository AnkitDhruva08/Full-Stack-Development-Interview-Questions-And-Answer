class NegativeNumberError(Exception):
    def __init__(self, number):
        self.number = number
        super().__init__(f"Negative number not allowed: {number}")

try:
    num = int(input("Enter a positive number: "))
    if num < 0:
        raise NegativeNumberError(num)
    print("You entered:", num)

except NegativeNumberError as e:
    print("Custom Exception Caught:", e)
