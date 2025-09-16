"""
N+1 problem: 1 query for main table + N queries for related objects.
🔹 What is the N+1 Problem?

Occurs when your code executes 1 query to fetch the main objects + N queries to fetch related objects.

It usually happens with ForeignKey, OneToOneField, or ManyToManyField relationships.
"""


# Suppose you have Departments and Employees:
class Department(models.Model):
    name = models.CharField(max_length=50)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


# Bad Code (causes N+1 queries)

employees = Employee.objects.all()  # 1 query
for emp in employees:
    print(emp.name, emp.department.name)  # N queries for departments



"""
Queries executed:

1 query to fetch all employees

1 query per employee to fetch department

If there are 1000 employees → 1001 queries → very slow!
"""


# Good Code (optimized with select_related)
employees = Employee.objects.select_related('department').all()
for emp in employees:
    print(emp.name, emp.department.name)









"""
| Problem                     | Solution                                   |
| --------------------------- | ------------------------------------------ |
| N+1 queries (slow)          | Use `select_related` for FK/OneToOne       |
| N+1 queries on M2M          | Use `prefetch_related`                     |
| Avoid loops causing queries | Fetch everything with QuerySet efficiently |

"""


# Many-to-Many Example

class Project(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project)


# BAD Code (causes N+1 queries)
employees = Employee.objects.all()
for emp in employees:
    for proj in emp.projects.all():  # triggers N queries for each employee
        print(proj.title)


# GOOD Code (optimized with prefetch_related)
employees = Employee.objects.prefetch_related('projects').all()
for emp in employees:
    for proj in emp.projects.all():  # no extra queries
        print(proj.title)


"""
⚡ Memory Tip:

1 query for main objects + N queries for related objects = N+1 problem

Always check select_related (FK/OneToOne) & prefetch_related (M2M / reverse FK)
"""