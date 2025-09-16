# createCsv.py

import csv

# File name
filename = "employees.csv"

# Data with headers
header = ["Name", "Age", "Gender", "Salary"]
rows = [
    ["John", 25, "Male", 50000],
    ["Alice", 30, "Female", 55000],
    ["Bob", 22, "Male", 40000],
    ["Eve", 35, "Female", 70000]
]

# Writing CSV
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    
    # Write header first
    writer.writerow(header)
    
    # Write multiple rows
    writer.writerows(rows)

print(f"✅ CSV file '{filename}' created successfully with headers!")
