from django.contrib import admin
from .models import User, Publisher, Book

# Register your models here.
admin.site.register(User)
admin.site.register(Publisher)
admin.site.register(Book)