"""🔹 What is ASGI?

2️⃣ ASGI (Asynchronous Server Gateway Interface)
🔹 What is ASGI?

Next-generation interface for Python web apps.

Supports async operations, HTTP, WebSockets, and other protocols.

Needed for real-time apps (chat, notifications, async APIs)."""


""""🔹 How it works
🔹 How it works

Browser (or client) sends HTTP or WebSocket request to ASGI server (e.g., Uvicorn, Daphne).

ASGI server passes request to Django via ASGI interface.

Django can handle async operations without blocking.

Response or WebSocket message is sent back to client.
Browser sends HTTP or WebSocket request to ASGI server (e.g., Daphne, Uvicorn).
ASGI server passes request to Django via ASGI.
Django processes request (can be async) and returns response.
ASGI server sends response back to browser.
Diagram:
Browser → ASGI Server (Daphne) → ASGI → Django → Response → Browser

"""

# myproject/asgi.py
# myproject/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_asgi_application()



"""This is similar to wsgi.py, but ASGI supports async.

To run Django with ASGI, you use an ASGI server like:

daphne myproject.asgi:application
# or
uvicorn myproject.asgi:application

🔹 WSGI vs ASGI
Feature	WSGI	ASGI
Type	Synchronous	Asynchronous & synchronous
Protocols	HTTP only	HTTP + WebSocket + custom
Use Case	Classic web apps	Real-time apps / async APIs
Servers	Gunicorn, uWSGI	Daphne, Uvicorn
🔹 Example Use Case (WebSocket)"""
# consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        self.send(text_data=json.dumps({"message": text_data}))


"""WebsocketConsumer only works with ASGI.

This allows real-time chat messages without refreshing the page."""



"""
⚡ Memory Tip:
WSGI = classic Django apps (blocking, sync)

ASGI = modern Django apps (async, real-time, WebSockets)

If you want, I can also explain the difference between wsgi.py and asgi.py in a Django project with a simple diagram so you can visualize how requests flow.

Do you want me to do that?"""









"""
| Pros                                   | Cons                        |
| -------------------------------------- | --------------------------- |
| Supports async operations              | Slightly more complex setup |
| Handles WebSockets                     | Not needed for simple apps  |
| Real-time applications possible        |                             |
| Compatible with HTTP & other protocols |                             |

"""


"""
🔹 Pros and Cons

| Feature          | WSGI                     | ASGI                          |
| ---------------- | ------------------------ | ----------------------------- |
| Type             | Synchronous              | Asynchronous & synchronous    |
| Protocols        | HTTP only                | HTTP + WebSocket + custom     |
| Server Examples  | Gunicorn, uWSGI          | Uvicorn, Daphne               |
| Use Case         | Classic web apps         | Real-time apps / async APIs   |
| Request Handling | Blocking / one at a time | Async / multiple concurrently |
| Django Default   | Before 3.0               | Django 3.0+ supports ASGI     |

"""


"""⚡ Memory Tip:
WSGI = classic Django apps (blocking, sync)
ASGI = modern Django apps (async, real-time, WebSockets)
"""

"""
🔹 When to use which?

Use WSGI:

Simple web apps

Standard HTML websites

No WebSockets or async needed

Use ASGI:

Real-time apps (chat, notifications)

Async tasks and APIs

WebSocket-based communication
"""


"""
⚡ Memory Tip:

WSGI = “Old reliable car” 🚗 → synchronous, only HTTP.

ASGI = “Modern Tesla” ⚡ → async, real-time, multi-protocol.
"""
