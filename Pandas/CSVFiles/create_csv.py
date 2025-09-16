"""

creating csv files via using python in dynamically way
in files mainly two types of files
read files 
write files
"""

import pandas as pd
import os 

filename = input("Enter file name: ").strip()

with open(filename, "w") as f:
    f.write("This is a dynamically created file.\n")

print(f"✅ File '{filename}' created successfully!")