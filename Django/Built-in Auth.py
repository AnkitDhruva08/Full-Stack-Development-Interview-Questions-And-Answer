"""
1️⃣ What Django Built-in Auth Provides

Django comes with django.contrib.auth which includes:

User model (django.contrib.auth.models.User)

Authentication functions: authenticate(), login(), logout()

Permissions and groups

Decorators: @login_required

Password hashing (secure by default)

✅ This saves you from manually handling passwords, hashing, and sessions.
"""


"""
2️⃣ Basic Setup

Make sure django.contrib.auth and django.contrib.sessions are in INSTALLED_APPS (default in Django projects).
"""

# settings.py
INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
]



# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Protected view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})



"""
👉 Instance methods use self (object data).
👉 Static methods use parameters only (no self).

Do you want me to also include a class method (@classmethod) example here, so you see all three
"""


class Calculator:
    company = "SuperCalc"  # Class variable

    def __init__(self, a, b):
        self.a = a  # Instance variable
        self.b = b

    # ✅ Instance method (works with object data)
    def add(self):
        return self.a + self.b

    # ✅ Instance method
    def subtract(self):
        return self.a - self.b

    # ✅ Static method (does not depend on object or class data)
    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def divide(x, y):
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y

    # ✅ Class method (works with class data, not instance)
    @classmethod
    def info(cls):
        return f"This calculator belongs to {cls.company}"


# 🔹 Example usage
calc = Calculator(10, 5)

# Instance methods
print("Addition:", calc.add())           # 15
print("Subtraction:", calc.subtract())   # 5

# Static methods
print("Multiplication:", Calculator.multiply(10, 5))  # 50
print("Division:", Calculator.divide(10, 5))          # 2.0

# Class method
print(Calculator.info())                 # This calculator belongs to SuperCalc
