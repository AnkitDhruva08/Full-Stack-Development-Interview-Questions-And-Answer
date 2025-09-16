"""
What is it APIVIEW?

APIView is the base class in DRF for creating class-based views for APIs.

It’s similar to Django’s View class but specialized for REST APIs (handles requests and returns JSON).

Why use it?

Gives you full control over logic for each HTTP method (GET, POST, PUT, DELETE).

Good when you want custom behavior.
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import Employee
from myapp.serializers import EmployeeSerializer

class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



"""
Pros: Complete flexibility.

Cons: You have to write a lot of repetitive code (especially for CRUD).
"""
