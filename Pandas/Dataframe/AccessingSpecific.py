"""
AccessingSpecific.py
5. Accessing Specific Cells with at and iat

If you need to access a specific cell, you can use 
the .at[] method for label-based indexing and the .iat[] method for integer position-based indexing.
These are optimized for fast access to single values.
"""

import pandas as pd

data = {'Name': ['John', 'Alice', 'Bob', 'Eve', 'Charlie'], 
        'Age': [25, 30, 22, 35, 28], 
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 
        'Salary': [50000, 55000, 40000, 70000, 48000]}

df = pd.DataFrame(data)
print("\nFull DataFrame:\n", df)

# Access the 'Salary' of the row with label 2
salary_at_index_2 = df.at[2, 'Salary']



# Access Salary at row index 2 (3rd row, Bob)
salary_at_index_2 = df.iloc[2]['Salary']
print('salary_at_index_2 :::::', salary_at_index_2)

# Sort by Salary column
filtered_salary = df[['Salary']].sort_values(by='Salary')
print("\nFiltered Salary (sorted):\n", filtered_salary)