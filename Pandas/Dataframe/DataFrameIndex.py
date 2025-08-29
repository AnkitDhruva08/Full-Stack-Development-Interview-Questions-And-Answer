import pandas as pd 

data = {
    'Name': ['John', 'Alice', 'Bob', 'Eve', 'Charlie'],
    'Age': [25, 30, 22, 35, 28],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'Salary': [50000, 55000, 40000, 70000, 48000]
}

df = pd.DataFrame(data, columns=["Name", "Age", "Gender", "Salary"])
print(df)
print("Default Index:", df.index)

# ✅ Set custom index using Name
df_index = df.set_index("Name")
print("\nCustom Index DataFrame:\n", df_index)

# Reset index back to default
reset_df_index = df.reset_index()
print("\nReset Index:\n", reset_df_index)

# ✅ Access particular row when Name is index
row = df_index.loc['Alice']  
print("\nRow for Alice:\n", row)

# ✅ Alternative: Access by row number (iloc)
row2 = df.iloc[1]   
print("\nRow by position (iloc[1]):\n", row2)
