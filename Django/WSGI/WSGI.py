"""1️⃣ WSGI (Web Server Gateway Interface)
🔹 What is WSGI?

Standard interface between Python web applications and web servers.

Designed for synchronous HTTP requests.

Django used WSGI by default before async support.

🔹 How it works

Browser sends an HTTP request to the web server (e.g., Gunicorn, uWSGI).

Web server passes the request to Django via WSGI.

Django processes the request (blocking) and returns an HTTP response.

Web server sends the response back to the browser.

Diagram:

Browser → Web Server (Gunicorn) → WSGI → Django → Response → Browser

🔹 WSGI Example in Django"""
# myproject/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_wsgi_application()


"""The application object is called by the WSGI server for every request.

Handles only HTTP requests, synchronously.

🔹 Pros and Cons
Pros	Cons
Simple & stable	Only synchronous (blocking)
Works with all Django apps	Cannot handle WebSockets
Well-supported by servers	Cannot do async tasks natively"""