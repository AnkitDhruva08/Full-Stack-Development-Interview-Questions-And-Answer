import pandas as pd

# File name
file_name = "Employee.xlsx"

# Data with headers
header = ["Name", "Age", "Gender", "Salary"]
rows = [
    ["John", 25, "Male", 50000],
    ["Alice", 30, "Female", 55000],
    ["Bob", 22, "Male", 40000],
    ["Eve", 35, "Female", 70000]
]

# Create DataFrame
df = pd.DataFrame(rows, columns=header)

# Save to Excel
df.to_excel(file_name, index=False)

print(f"Excel file '{file_name}' created successfully ✅")
