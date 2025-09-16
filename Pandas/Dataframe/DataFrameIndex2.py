import pandas as pd 


# function for auto type case of value
def auto_cast(value: str):
    """Convert to int, float, or keep as string"""
    value = value.strip()
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value

column_count = int(input("Enter how many columns you want: "))
data = {}
for i in range(column_count):
    column_name = input(" Enter Column Name  ::: \n")
    raw_values = input(f"Enter values for {column_name} ::: \n").split(',')
    column_values = list(map(auto_cast, raw_values))
    data[column_name] = column_values



print('\n Data ===<<<>> :: \n', data)



# create dataframe
df = pd.DataFrame(data)

index_col = input("\nEnter column name you want to set as index ::: ")
if index_col in df.columns:
    df.set_index(index_col, inplace=True)

print("\nFinal DataFrame:\n", df)



# ✅ Access particular row when some column is set as index
row_key = input("\nEnter the index value you want to access row data ::: ").strip()
row_key_casted = auto_cast(row_key)

if row_key_casted in df.index:
    row_data = df.loc[row_key_casted]
    print(f"\nRow data for '{row_key_casted}':\n", row_data)
else:
    print(f"\n'{row_key}' not found in index!")



