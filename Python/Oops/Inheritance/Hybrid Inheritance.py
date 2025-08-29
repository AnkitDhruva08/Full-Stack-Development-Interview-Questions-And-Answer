class Person:
    def __init__(self, name):
        self.name = name

    def show_person(self):
        return f"Person Name: {self.name}"


class Father(Person):
    def __init__(self, name, father_job):
        Person.__init__(self, name)  
        self.father_job = father_job

    def show_father(self):
        return f"Father's Job: {self.father_job}"


class Mother(Person):
    def __init__(self, name, mother_hobby):
        Person.__init__(self, name)   
        self.mother_hobby = mother_hobby

    def show_mother(self):
        return f"Mother's Hobby: {self.mother_hobby}"


class Child(Father, Mother):
    def __init__(self, name, father_job, mother_hobby, school):
        Father.__init__(self, name, father_job)   
        Mother.__init__(self, name, mother_hobby) 
        self.school = school

    def show_child(self):
        return f"Child studies at: {self.school}"


# Main Program
c = Child("Ankit", "Engineer", "Gardening", "DPS School")

print(c.show_person()) 
print(c.show_father()) 
print(c.show_mother()) 
print(c.show_child())   
