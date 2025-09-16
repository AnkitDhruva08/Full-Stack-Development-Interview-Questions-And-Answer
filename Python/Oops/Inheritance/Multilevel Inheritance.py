class School:
    def show(self):
        return "I'M in School Class"
    

class Teacher(School):
    def disp(self):
        return "I'M in  Teacher class"
    
class Student(Teacher):
    def disp_std(self):
        return "I'M in  Student class"
    
    


# main program
s = Student()

print(s.show())
print(s.disp())
print(s.disp_std())