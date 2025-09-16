lower_range = int(input("Enter lower range: "))
upper_range = int(input("Enter upper range: "))
print(f"Prime numbers between {lower_range} and {upper_range} are:")

lst = [] 

for num in range(lower_range, upper_range + 1):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                break
        else:
            lst.append(num)


print(lst)