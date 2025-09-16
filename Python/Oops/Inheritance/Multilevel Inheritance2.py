# multilevel inheritance 


class School:
    def __init__(self, school_name):
        self.school_name = school_name

    def disp_school(self):
        return self.school_name
    
class Teacher(School):
    def __init__(self, school_name, teache_name):
        super().__init__(school_name)
        self.teache_name = teache_name

    def disp_teach(self):
        teacher_details = {
            "school_name": self.school_name,
            "teache_name": self.teache_name
            
        }
        return teacher_details


class Students(Teacher):
    def __init__(self, school_name, teache_name, std_name):
        super().__init__(school_name, teache_name)
        self.std_name = std_name


    def disp_std(self):
        students_details = {
            "school_name": self.school_name,
            "teache_name": self.teache_name,
            "std_name" : self.std_name
        }

        return students_details
    


# main program 
s = Students("Green Valley School", "Mr. Sharma",  "Ankit")
print(s.disp_school())
print(s.disp_teach())
print(s.disp_std())
