"""
🔹 What is a Model in Django?

A Model in Django is a Python class that represents a table in your database.

Each attribute of the model = a column in that table.

Each instance (object) of the model = a row in that table.
"""


from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)   # column: name (varchar)
    age = models.IntegerField()               # column: age (int)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.name



"""
Django supports 3 main types of relationships:
"""

"""🔹 1. One-to-One (One row ↔ One row)

Use when each object is related to exactly one object.

Example: Every User has exactly one Profile."""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField()



# 👉 If user is deleted, profile is also deleted (because of CASCADE).
"""

🔹 2. One-to-Many (ForeignKey)

Most common: each object belongs to one parent, but parent can have many children.

Example: One Department has many Employees."""

class Department(models.Model):
    name = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  


# 👉 SQL: employee.department_id → department.id



it = Department.objects.create(name="IT")
emp = Employee.objects.create(name="Ankit", department=it)

print(emp.department.name)       # "IT"
print(it.employee_set.all())     # All employees in IT

"""🔹 3. Many-to-Many

Use when both sides can have many.

Example: An Employee can work on many Projects, and a Project can have many Employees."""

class Project(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project)



p1 = Project.objects.create(title="Django App")
p2 = Project.objects.create(title="AI System")

emp = Employee.objects.create(name="Ankit")
emp.projects.add(p1, p2)  # Add multiple projects

print(emp.projects.all())  # [Django App, AI System]
print(p1.employee_set.all())  # Employees in project
