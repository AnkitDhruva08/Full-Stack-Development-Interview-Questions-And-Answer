"""1. One-to-One (OneToOneField)"""
class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()



# Query
profile = Profile.objects.select_related('user').get(id=1)
print(profile.user.username)

"""Performance Notes

OneToOneField is essentially a ForeignKey with unique=True.

Use select_related to fetch the related object in the same SQL query (JOIN).

Without select_related, Django will execute a separate query for each profile, leading to N+1 query problem."""






# -----------------------------------------------------------------
"""2. One-to-Many (ForeignKey)"""
class Department(models.Model):
    name = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)




# Query
employees = Employee.objects.select_related('department').all()
for emp in employees:
    print(emp.department.name)


"""Performance Notes
Each ForeignKey is one-to-many: child → parent.

Use select_related for parent objects to avoid extra queries.

Iterating without select_related will trigger a query per employee for the department.

Example: 100 employees → 1 query for employees + 100 queries for departments if not select_related."""

# -------------------------------------------------------------------------------------------------------

"""Performance Notes
3. Many-to-Many (ManyToManyField)

Many-to-Many uses a join table in the database.

Use prefetch_related for many-to-many relations.

This executes two queries instead of one per employee:

Fetch all employees

Fetch all related projects in one query

Without prefetch_related, Django will execute a query per employee for projects → N+1 query problem."""


class Project(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project)



# Query
employees = Employee.objects.prefetch_related('projects').all()
for emp in employees:
    for proj in emp.projects.all():
        print(proj.title)
