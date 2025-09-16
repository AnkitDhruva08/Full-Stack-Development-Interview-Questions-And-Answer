"""
4. AccessingRowsBasedonConditions

Pandas allows you to filter rows based on conditions, which can be very powerful for exploring subsets of data that meet specific criteria.
"""


import pandas as pd

data = {'Name': ['John', 'Alice', 'Bob', 'Eve', 'Charlie'], 
        'Age': [25, 30, 22, 35, 28], 
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 
        'Salary': [50000, 55000, 40000, 70000, 48000]}

df = pd.DataFrame(data)
print("\nFull DataFrame:\n", df)

print(':::::::::::::<<<<<>>>>',df['Age'])
filtered_data = df[df['Age'] > 25]
print('filtered_data ===<<<>>>', filtered_data)