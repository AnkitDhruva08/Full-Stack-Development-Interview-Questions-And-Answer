filename = "myfile.txt"

with open(filename, "w") as f:  
    f.write("Hello, this is the first line.\n")
    f.write("This is the second line.\n")

print(f"✅ Data inserted into {filename}")