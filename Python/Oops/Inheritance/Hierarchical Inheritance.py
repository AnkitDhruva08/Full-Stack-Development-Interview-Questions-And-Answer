# Parent Class
class Parent:
    def __init__(self, parent_name):
        self.parent_name = parent_name


# Child 1
class Child1(Parent):
    def __init__(self, parent_name, first_child):
        super().__init__(parent_name)   
        self.first_child = first_child

    def disp_child1(self):
        return {
            "parent_name": self.parent_name,
            "first_child": self.first_child
        }


# Child 2
class Child2(Parent):
    def __init__(self, parent_name, second_child):
        super().__init__(parent_name)
        self.second_child = second_child

    def disp_child2(self):
        return {
            "parent_name": self.parent_name,
            "second_child": self.second_child
        }


# main program
C1 = Child1("Dhruva", "Ankit")
print(C1.disp_child1())

C2 = Child2("Dhruva", "Rinku")
print(C2.disp_child2())
