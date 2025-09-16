class Student:
    # Instance method to read data
    def read_data(self, name, age):
        print("Inside read_data function...")
        self.name = name
        self.age = age

    # Instance method to display data
    def disp_data(self):
        print("Inside disp_data function...")
        result_data = [self.name, self.age]
        print('result_data ==<<>>>', result_data)
        return result_data


# ---- Main Program ----
name = input("Enter student name ::: ")
age = int(input("Enter age ::: "))

# Create object
s = Student()

# Call instance methods
s.read_data(name, age)
s.disp_data()
