class Employee:
    company_name = "Atlantick Solutions"

    @classmethod
    def company(cls):
        return cls.company_name 
    
    def empoyee_details(self, name, salary):
        self.name = name 
        self.salary = salary 

    
    def disp_details(self):
        details = {
            "name" : self.name ,
            "salary" :  self.salary,
            " company name" :  Employee.company_name
        }

        return details
    




# main program 
e = Employee()

e.empoyee_details("ankit", 50000)
print(e.disp_details())