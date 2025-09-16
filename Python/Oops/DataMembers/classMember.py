class Student : 
    school = "sarswati school pahadi khera"



s = Student()
s.name = "Ankit"
for k, v in s.__dict__.items():
    print(f"{k} ====<<<>>>> {v}")

print("Class dict:", Student.__dict__)  

