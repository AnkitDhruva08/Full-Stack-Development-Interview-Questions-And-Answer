class Student: pass

s = Student
print("s =<<>>", s)
s.name = "ankit"
s.age= 20

print("s =<<>>", s.__dict__)
print('name ==<<>>', s.name)