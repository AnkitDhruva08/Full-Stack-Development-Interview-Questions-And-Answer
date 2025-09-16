"""
What you need to do for custom auth

Custom User Model (optional, if you don’t want django.contrib.auth.User)

Password hashing / verification

Sessions or Tokens (to keep user logged in)

Middleware or decorators to protect views
"""


# Custom Authentication with Email & Password
from django.db import models
import hashlib

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    name = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    
    def check_password(self, raw_password):
        return self.password_hash == hashlib.sha256(raw_password.encode()).hexdigest()



# views.py
from django.shortcuts import render, redirect
from .models import CustomUser

# Login view
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id  # manually manage session
                return redirect('dashboard')
            else:
                error = "Invalid credentials"
        except CustomUser.DoesNotExist:
            error = "User not found"
        return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    request.session.flush()  # clear session
    return redirect('login')

# Protected view
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'dashboard.html', {'user': user})



# login.html 

"""
<form method="post">
  {% csrf_token %}
  <input type="email" name="email" placeholder="Email">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
  {% if error %}<p>{{ error }}</p>{% endif %}
</form>

"""


"""
3️⃣ How it works

User submits email & password.

You hash the password and compare with stored hash (check_password).

If valid, store user_id in session (or return a token for API).

To protect pages, check if user_id exists in session.
"""


# 4️⃣ Optional: Token-Based Auth (for APIs)

import secrets

class AuthToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

def generate_token(user):
    token = secrets.token_hex(32)
    AuthToken.objects.create(user=user, token=token)
    return token



"""
| Feature         | Custom Auth without Django built-in  |
| --------------- | ------------------------------------ |
| User Model      | Your own `CustomUser`                |
| Password        | Hash manually (e.g., SHA256, bcrypt) |
| Session         | `request.session` for web            |
| Token           | Custom token model for API auth      |
| View Protection | Check session / token manually       |

"""