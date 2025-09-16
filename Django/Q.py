"""
🔹 What is Q in Django?

Q is a class in django.db.models used to make complex WHERE clauses.

Normally, filter() combines conditions with AND.

With Q, you can combine them with OR, AND, and NOT more flexibly.
"""

from django.db.models import Q 



# Example Without Q
Employee.objects.filter(name="Ankit", department="IT")


# Example With Q (OR condition)

# Employees whose name is "Ankit" OR department is "IT"
Employee.objects.filter(
    Q(name="Ankit") | Q(department="IT")
)


"""SELECT * FROM employee WHERE name = 'Ankit' OR department = 'IT';"""