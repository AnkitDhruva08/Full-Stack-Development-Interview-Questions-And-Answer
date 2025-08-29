class Parent:
    def show(self):
        return "I'M in Parent Class"
    

class Child(Parent):
    def disp(self):
        return "Child class"
    


# main program
c = Child()

print(c.show())
print(c.disp())