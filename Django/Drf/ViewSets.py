"""
2️⃣ ViewSets
What is it?

ViewSet is an abstraction over APIView for CRUD operations.

DRF automatically provides list, create, retrieve, update, destroy methods.

Works with routers to generate URLs automatically.

Why use it?

Great for standard CRUD APIs — you don’t have to write repetitive code.

Less boilerplate, cleaner code.
"""

from rest_framework import viewsets
from myapp.models import Employee
from myapp.serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
