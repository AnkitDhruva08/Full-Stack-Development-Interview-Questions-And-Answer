#DestEx2.py
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
print("\nProgram execution completed:")