"""
🧠 What is a Signal?

A signal in Django is a messaging system that allows decoupled parts of your application to get notified when certain actions occur.

Think of it like a listener: when something happens, the signal “fires” and any connected functions are called automatically.

It helps in loosely coupling code so that one part doesn’t need to directly call another.
"""


"""
🔹 Why Do We Use Signals?

Signals are useful when you want to perform actions automatically after certain events, such as:

Creating a profile when a new user is created.

Sending email notifications after a model is saved.

Logging changes in the database.

Instead of manually calling functions in every view, signals allow automatic execution on events.
"""


"""
🔹 Common Django Signals

| Signal        | When it fires                               |
| ------------- | ------------------------------------------- |
| `pre_save`    | Before a model instance is saved            |
| `post_save`   | After a model instance is saved             |
| `pre_delete`  | Before a model instance is deleted          |
| `post_delete` | After a model instance is deleted           |
| `m2m_changed` | When a many-to-many relationship is changed |

"""


# 🔹 How to Use Signals in Django
# Example: Create a user profile automatically
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals  # Make sure signals are imported


"""@receiver(post_save, sender=User) → listens for post_save on User.

Function runs automatically when a new User is created.

🔹 If You Don’t Want to Use Signals

You can call functions directly in your views or serializers instead of signals.

Example: instead of relying on post_save to create a profile:

user = User.objects.create(username='Alice')
Profile.objects.create(user=user)  # manually create profile"""


"""Pros of skipping signals:

Code is more explicit and easier to trace.

Less “magic” happening behind the scenes.

Cons:

You have to remember to call the function everywhere the event can happen.

Harder to maintain in large projects.
"""
"""✅ Summary

Signal → a way to listen to events and run code automatically.

Use case → decoupled logic like auto-creating related models, sending emails, logging, etc.

Alternative → manually call functions in views/serializers if you want full control.

If you want, I can make a diagram showing how signals work in Django to make it very visual.

Do you want me to do that?"""