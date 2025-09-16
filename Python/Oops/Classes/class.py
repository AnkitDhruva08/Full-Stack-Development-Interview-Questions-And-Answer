class Student:
    def read_data(self):
        self.name = input("Enter student name :: ")
        self.roll_num = int(input("Enter roll number ::: "))
        self.age = int(input("Enter Age ::: "))

    
    def disp_values(self):
        print("Name :::::", self.name)
        print('Roll Number ::::', self.roll_num)
        print("Age ::::", self.age)



# main function 
S = Student()
S.read_data()
S.disp_values()