# Define custom exception
class InvalidAgeError(Exception):
    pass

# Use custom exception
age = int(input("Enter age: "))

if age < 18:
    raise InvalidAgeError("Age must be 18 or above to vote.")
else:
    print("You are eligible to vote.")
