def my_dec(func):
    def wrapper(a, b):
        result = func(a, b)   # call the original function
        substract = a - b
        print("Subtraction:", substract)
        return result         # return the original function's result
    return wrapper

@my_dec
def say_hello(a, b):
    return a + b

print("Addition:", say_hello(10, 2))
