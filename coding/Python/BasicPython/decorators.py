def decorators(func):
    def wrapper():
        result = func()
        print("Hello")
        return result
    
    return wrapper
    

@decorators
def my_fun():
    result = "Ankit Mishra"
    return result



print(my_fun())