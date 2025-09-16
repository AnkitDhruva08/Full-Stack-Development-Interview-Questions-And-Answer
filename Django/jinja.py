"""
Jinja (or Jinja2) is a templating engine for Python.

It lets you generate HTML dynamically by combining HTML templates with data from Python.

Think of it as Python code embedded in HTML, but safe and structured.
"""


"""🔹 Key Features

Template Variables

<p>Hello, {{ name }}!</p>


{{ name }} is replaced with the Python variable name.

Control Structures

{% if user.is_authenticated %}
  <p>Welcome, {{ user.username }}!</p>
{% else %}
  <p>Please log in.</p>
{% endif %}


Loops

<ul>
{% for employee in employees %}
  <li>{{ employee.name }} - {{ employee.department }}</li>
{% endfor %}
</ul>


Filters

<p>{{ message|upper }}</p>   <!-- Converts message to uppercase -->


Common filters: lower, upper, length, default, date, etc.

Template Inheritance

<!-- base.html -->
<html>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

<!-- home.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Home Page</h1>
{% endblock %}

🔹 Why Jinja is Useful

Separates Python logic from HTML presentation → cleaner code.

Safe: automatically escapes HTML to prevent XSS attacks.

Powerful: supports loops, conditionals, macros, template inheritance.

Works in both Flask (default) and Django (similar syntax).

🔹 Example in Python
from jinja2 import Template

template = Template("<p>Hello, {{ name }}!</p>")
html = template.render(name="Ankit")
print(html)  # Output: <p>Hello, Ankit!</p>


⚡ Memory Tip:

{{ }} → output a variable

{% %} → run a Python-like statement (if, for, etc.)

{{ variable|filter }} → apply filters"""