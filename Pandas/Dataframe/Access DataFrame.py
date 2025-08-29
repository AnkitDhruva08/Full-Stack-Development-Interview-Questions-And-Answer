import pandas as pd

data = {'Name': ['John', 'Alice', 'Bob', 'Eve', 'Charlie'], 
        'Age': [25, 30, 22, 35, 28], 
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'], 
        'Salary': [50000, 55000, 40000, 70000, 48000]}

df = pd.DataFrame(data)
print("\nFull DataFrame:\n", df)

# Accessing Columns From DataFrame
column_name = input("\nEnter Column Name to access the column :: \n")
print("\nSelected Column:\n", df[column_name])

# Set index to the selected column
df = df.set_index(column_name)


print("\nRows 0, 2, 4:\n", df.iloc[[0, 2, 4]])

print("\nDataFrame with new index:\n", df)

row_index = input("\nEnter row index value to access row data :: \n").strip()

# detect row accoring to thier type 

if df.index.inferred_type == "integer":
    try:
        row_index = int(row_index)
         
    except ValueError:
        pass

if df.index.inferred_type == "floating":
    try:
        row_index = float(row_index)
         
    except ValueError:
        pass


# finding the row 
if row_index in df.index:
    df = df.loc[row_index]
    print('df ==<<>> ::', df)



