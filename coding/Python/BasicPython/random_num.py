import random 

num = int(input("Enter a number: "))

attempts = 0

while True:
    rand_num = random.randint(0, num)  
    attempts += 1
    print("Generated:", rand_num)
    
    if rand_num == num:
        print(f"🎉 Number {num} found in {attempts} attempts!")
        break
