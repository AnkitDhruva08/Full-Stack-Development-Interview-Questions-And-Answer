"""
These two (filter and get) are very common in Django ORM but they behave quite differently. Let’s break them down:

🔹 get()

Purpose: Fetch exactly one object from the database.

Usage:

obj = Model.objects.get(field=value)


Returns:

A single object.

Errors:

Raises DoesNotExist if no object is found.

Raises MultipleObjectsReturned if more than one object matches.

👉 Use it when you are sure there’s only one match.

Example:
from myapp.models import Employee

emp = Employee.objects.get(id=1)
print(emp.name)


If no employee with id=1 exists → ❌ error.
If more than one exists (shouldn’t happen with id) → ❌ error.

🔹 filter()

Purpose: Fetch multiple objects (zero, one, or many).

Usage:

queryset = Model.objects.filter(field=value)


Returns:

A QuerySet (like a list of objects).

Errors:

Never raises an error. If no objects match, returns an empty QuerySet.

👉 Use it when you want a list of results or are not sure how many will match.

Example:
emps = Employee.objects.filter(department="IT")
for e in emps:
    print(e.name)


If no employees in IT → just an empty list, no error.

🔑 Difference Between get() vs filter()
Feature	get()	filter()
Returns	Single object	QuerySet (0, 1, or many)
Error if no match?	Yes (DoesNotExist)	No (returns empty set)
Error if many?	Yes (MultipleObjectsReturned)	No
When to use	When you know there’s exactly one	When you expect many
🔹 Example Side by Side
# Suppose Employee table has:
# (id=1, name="Ankit")
# (id=2, name="Mishra")

# get()
emp = Employee.objects.get(id=1)  
print(emp.name)   # ✅ "Ankit"

# filter()
emps = Employee.objects.filter(name="Mishra")  
print(emps)       # ✅ <QuerySet [<Employee: Mishra>]>


If you try:

Employee.objects.get(name="Unknown")  


👉 Raises DoesNotExist.

But:

Employee.objects.filter(name="Unknown")


👉 Returns [] (empty QuerySet).

⚡ Memory Tip:

get = “Give me one” (error if not one).

filter = “Give me a list” (safe, even if empty).
"""