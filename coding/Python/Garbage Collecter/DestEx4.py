#DestEx4.py
class Emp:
	def  __init__(self,eno,ename,sal):
		self.eno=eno
		self.ename=ename
		self.sal=sal
		print(self.eno,self.ename,self.sal)
	
	def  __del__(self):
		print("GC calls __del__() for de-allocating mem space:")

#main program
print("Program execution started:")
print("\ncontent of e1")
e1=Emp(10,"RS",1.2)
print("No longer interested to maintain memory space of e1")
e1=None # GC automatically calls __del__(self)---forcefully calling GC
print("\ncontent of e2")
e2=Emp(20,"DR",2.2)
print("No longer interested to maintain memory space of e2")
e2=None # GC automatically calls __del__(self)---forcefully calling GC
print("\ncontent of e3")
e3=Emp(30,"TR",3.2)
print("No longer interested to maintain memory space of e3")
e3=None # GC automatically calls __del__(self)---forcefully calling GC
print("\nProgram execution completed:")
