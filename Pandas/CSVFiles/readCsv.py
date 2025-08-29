

import pandas as pd

file_name = "employees.csv"


# reading csv files as raw data
with open(file_name, "r") as fp:
    print(fp.readlines())


# Read CSV with Pandas
df = pd.read_csv(file_name)



print("Before appending:\n", df)

# 🔹 New data to append (as dictionary or list of dictionaries)
new_data = {
    "Name": "Charlie",
    "Age": 28,
    "Gender": "Male",
    "Salary": 48000
}

# Convert to DataFrame
new_df = pd.DataFrame([new_data])

# Append to existing DataFrame
df = pd.concat([df, new_df], ignore_index=True)

# Save back to CSV
df.to_csv(file_name, index=False)

print("\nAfter appending:\n", df)