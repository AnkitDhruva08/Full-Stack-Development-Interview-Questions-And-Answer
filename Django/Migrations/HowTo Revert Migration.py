"""
🔹 How Django Migrations Work

Each migration file (0001_initial.py, 0002_add_field.py, 0003_auto.py, etc.) is a step in database schema history.

When you run migrate, Django moves the database schema to that step.


FOR DIPALY OF LIST OF MIGRATION python manage.py showmigrations


🔹 Example Migration History
0001_initial   ✅
0002_add_field ✅
0003_auto      ✅


If you want to remove the effects of 0003_auto, you don’t say "undo 0003".
Instead, you say "take me back to 0002".

👉 That’s why the command is:

python manage.py migrate app_name 0002



🔑 In Short

We use:

python manage.py migrate app_name 0002


to roll back 0003_auto because:

Django applies migrations sequentially.

To undo 0003, we tell Django to go back one step (0002).


"""