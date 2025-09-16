"""
🚀 — Model Inheritance in Django is just like Python class inheritance, but for Django models.
It allows you to create models that share common fields/behavior.

Django gives 3 types of model inheritance:
"""


"""1. Abstract Base Classes
Use when you want to put common information into a parent class that you don’t want to create a database table for.
The parent class is abstract, so no table is created for it.
Use when you want to put common fields in a parent class, but don’t want a table for it.

Only child models get their own tables.
"""

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # No table created for this

class Employee(BaseModel):
    name = models.CharField(max_length=100)

class Customer(BaseModel):
    email = models.EmailField()

# Department table has fields: id, name, created_at, updated_at
"""
2. Multi-Table Inheritance



Each model has its own database table.

Child has an implicit OneToOne relation with the parent.

Use when child models need extra fields but still relate to parent.
"""


class Person(models.Model):
    name = models.CharField(max_length=100)

class Student(Person):
    roll_no = models.CharField(max_length=20) 


s = Student.objects.create(name="Ankit", roll_no="101")
print(s.name)




"""
🔹 3. Proxy Models

Use when you want to change behavior (methods, default manager, ordering) of a model, but not create a new table.
"""

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class StudentProxy(Person):
    class Meta:
        proxy = True   # No new table

    def is_minor(self):
        return self.age < 18


"""👉 Only person table exists.
But you can call:"""

s = StudentProxy.objects.create(name="Ankit", age=17)
print(s.is_minor()) 


"""🔑 Summary Table
| Type                    | Creates Table?    | Use Case                        |
| ----------------------- | ----------------- | ------------------------------- |
| **Abstract Base Class** | ❌ (only children) | Share common fields             |
| **Multi-table**         | ✅                 | Extend models with extra fields |
| **Proxy**               | ❌                 | Change behavior, not schema     |

"""


"""
⚡ Memory Tip:

Abstract → just a blueprint.

Multi-table → real inheritance with new table.

Proxy → same table, new behavior.
"""