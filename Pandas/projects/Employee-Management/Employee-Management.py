import pandas as pd
import os

file_name = "employees.csv"

# Step 1: Initialize Data
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Name", "Age", "Gender", "Salary", "Active"])
    df.to_csv(file_name, index=False)

# Step 2: Menu
while True:
    print("\n--- Employee Data Manager ---")
    print("1. Add Employee")
    print("2. Update Employee")
    print("3. Delete Employee")
    print("4. Search Employee")
    print("5. Show All Employees")
    print("6. Exit")

    choice = input("Enter choice: ").strip()

    if choice == "1":  # Add Employee
        name = input("Name: ")
        age = int(input("Age: "))
        gender = input("Gender: ")
        salary = float(input("Salary: "))
        active = True

        new_row = {"Name": name, "Age": age, "Gender": gender, "Salary": salary, "Active": active}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name, index=False)
        print("✅ Employee Added")

    elif choice == "2":  # Update Employee
        search_name = input("Enter name to update: ")
        if search_name in df["Name"].values:
            print(df[df["Name"] == search_name])
            column = input("Which column to update (Age/Gender/Salary/Active)? ")
            new_val = input("Enter new value: ")

            if column in ["Age", "Salary"]:
                new_val = float(new_val)
            elif column == "Active":
                new_val = new_val.lower() == "true"

            df.loc[df["Name"] == search_name, column] = new_val
            df.to_csv(file_name, index=False)
            print("✅ Updated successfully")
        else:
            print("❌ Employee not found")

    elif choice == "3":  # Delete Employee
        search_name = input("Enter name to delete: ")
        df = df[df["Name"] != search_name]
        df.to_csv(file_name, index=False)
        print("✅ Deleted")

    elif choice == "4":  # Search Employee
        search_name = input("Enter name to search: ")
        print(df[df["Name"].str.contains(search_name, case=False)])

    elif choice == "5":  # Show All
        print(df)

    elif choice == "6":
        break

    else:
        print("❌ Invalid choice")
