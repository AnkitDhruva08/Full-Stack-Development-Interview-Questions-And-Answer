def generator_numbers():
    l = [1,2,3]

    for i in l:
        yield i
   

gen = generator_numbers()
print(next(gen)) 
print(next(gen)) 
print(next(gen)) 




def normal_numbers():
    l =  [1, 2, 3]

    for i in l:
        return i



nor = normal_numbers()
print(next(nor)) 
print(next(nor)) 
print(next(nor)) 
# Output: [1, 2, 3]