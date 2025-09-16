class Animal:
    def sound(self):
        return "Animal can speak"
    

class Dog(Animal):
    def sound(self):
        return "Dog Bark"
    


class Cat(Animal):
    def sound(self):
        return "meow"
    



# main program 
a = Animal()
print(a.sound())

d = Dog()

print(d.sound())

c = Cat()
print(c.sound())

animals = [Dog(), Cat()]
for i in animals:
    print("Sounds :::: ",i.sound())