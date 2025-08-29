class Student:
    crs = "python"

    @classmethod
    def disp_crs(cls):
        default_course = cls.crs
        return default_course

    
    @classmethod
    def update_crs(cls, new_cours):
        cls.crs = new_cours

        return new_cours
    


# main program 

s1 = Student()
print(s1.disp_crs())
print(s1.update_crs("java"))


