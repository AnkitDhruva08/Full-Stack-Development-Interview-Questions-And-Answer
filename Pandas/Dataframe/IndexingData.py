"""
IndexingData.py
1. Indexing Data using the [] Operator
The [] operator is the basic and frequently used method for indexing in Pandas. 
It allows us to select columns and filter rows based on conditions. This method can be used to select individual columns or multiple columns.

1. Selecting a Single Column
To select a single column, we simply refer the column name inside square brackets.
"""


import pandas as pd

data = {'Name': ['John', 'Alice', 'Bob', 'Eve', 'Charlie'], 
        'Age': [25, 30, 22, 35, 28], 
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 
        'Salary': [50000, 55000, 40000, 70000, 48000]}

df = pd.DataFrame(data)
values = data.get('Salary')
print('values ==<<<>', values)
retriveData = df.iloc[[2,1]]
print('retriveData =<<<>', retriveData)

first_max = second_max = float('-inf') 
for i in values:
    if i > first_max:
        second_max = first_max
        first_max = i 
    elif i > second_max and first_max != i:
        second_max = i


print('first_max ==<<<>', first_max)
print('Second Max ==<<>', second_max)
