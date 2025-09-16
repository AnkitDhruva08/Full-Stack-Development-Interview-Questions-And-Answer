"""custom_auth_project/
├── custom_auth_app/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── custom_auth_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── manage.py
"""


# models.py 
from django.db import models
import hashlib
import secrets

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    name = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    
    def check_password(self, raw_password):
        return self.password_hash == hashlib.sha256(raw_password.encode()).hexdigest()

class AuthToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_token(user):
        token = secrets.token_hex(32)
        AuthToken.objects.create(user=user, token=token)
        return token


# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CustomUser, AuthToken

# ----------- Web Session Auth -----------

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                error = "Invalid credentials"
        except CustomUser.DoesNotExist:
            error = "User not found"
        return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'dashboard.html', {'user': user})

# ----------- API Token Auth -----------

def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = request.POST
    try:
        user = CustomUser.objects.get(email=data['email'])
        if user.check_password(data['password']):
            token = AuthToken.generate_token(user)
            return JsonResponse({"token": token})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

def api_dashboard(request):
    token_value = request.headers.get("Authorization")
    if not token_value:
        return JsonResponse({"error": "Token missing"}, status=401)
    try:
        token = AuthToken.objects.get(token=token_value)
        user = token.user
        return JsonResponse({"message": f"Hello {user.name}"})
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)


# urls.py 
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # API endpoints
    path('api/login/', views.api_login, name='api_login'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
]



# login.html
"""
<form method="post">
  {% csrf_token %}
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
  {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
</form>

"""


"""
7️⃣ Security Notes

Passwords are hashed (SHA256 here for simplicity, but use bcrypt in production).

Tokens are random 64-character hex strings.

Session management handled manually.

This setup gives you:
✅ Custom user model
✅ Session-based auth for web pages
✅ Token-based auth for APIs
✅ No dependency on Django’s built-in auth system

If you want, I can also upgrade this project to:

Support password reset

Token expiration & refresh

Protect API views with decorators
"""