"""
🔹 What is DRF?

DRF stands for Django REST Framework.

It is a powerful and flexible toolkit for building Web APIs in Django.

With DRF, you can expose your Django models as RESTful endpoints that can be consumed by frontends (React, Angular, mobile apps, etc.).

It’s like Django but specialized for APIs instead of rendering HTML pages.
"""

"""
🔹 Key Features

1. Serializers – Convert Django models (Python objects) to JSON (or other content types) and vice versa."""

from rest_framework import serializers
from myapp.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'department']



""" 2.Views / ViewSets – Define API endpoints."""

from rest_framework import viewsets
from myapp.models import Employee
from myapp.serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



""" 3.Routers – Automatically generate URLs for your API."""

from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from myapp.views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
urlpatterns = router.urls



"""
4.Authentication & Permissions – Built-in support for token auth, JWT, session auth, custom permissions.
"""
"""
5.Browsable API – DRF gives a web interface to test your APIs in the browser, very useful for debugging.
"""


# Example 

# models.py
class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

# serializers.py
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# views.py
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# urls.py
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
urlpatterns = router.urls



"""
Now your API endpoints are ready:

GET /employees/ → list all employees

POST /employees/ → create a new employee

GET /employees/1/ → retrieve employee with ID 1

PUT /employees/1/ → update

DELETE /employees/1/ → delete
"""


"""
| Feature          | APIView                     | ViewSet                |
| ---------------- | --------------------------- | ---------------------- |
| URL Routing      | Manual                      | Automatic with Routers |
| CRUD Boilerplate | Must write each method      | Provided automatically |
| Flexibility      | High                        | Medium (mostly CRUD)   |
| Use Case         | Custom APIs / complex logic | Standard CRUD APIs     |

"""

"""
⚡ Memory Tip:

APIView = “I want total control over every request.”

ViewSet = “I want standard CRUD APIs fast, with less code.”
"""