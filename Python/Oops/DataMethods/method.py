class Employee:
    company_name = input("Enter Company Name ::: ")

    @classmethod
    def display_cpmpany(cls):
        return cls.company_name 
    
    # instance member for employe details 

    def employee_details(self, name, salary, experience):
        self.name = name 
        self.salary = salary
        self.experience = experience

    def disp_details(self):
        details = {
            "Name": self.name,
            "Salary": self.salary,
            "Experience" : self.experience,
            "company_name" : Employee.company_name

        }

        return details 
    

    # 🔹 Static method 
    @staticmethod
    def is_valid_salary(salary):
        if salary > 5000:
            return salary 

    @staticmethod 
    def is_valid_experience(experience):
        if experience > 2:
            return experience
        



# main program 

name = input("Enter Name ::: ")
salary = int(input("enter Salary ::: "))
experience = float(input("enter Experience ::: "))
e = Employee() 

if e.is_valid_salary(salary) and e.is_valid_experience(experience):
    e.employee_details(name, salary, experience)
    print('Employee.disp_details() ==<<>', e.disp_details())


else:
    print("Salary is less than 5000")
        
    
    
    