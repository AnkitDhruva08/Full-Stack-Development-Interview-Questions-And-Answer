arr = list(map(int, input('Enter List of Values :: ').split(',')))
print('arr ==<<<>>', arr)

sub_arry = []

for i in range(len(arr) - 1):
    for j in range(i +1, len(arr) - 1):
        sub = arr[ i:j + 1]
        sub_arry.append(sub)



print('sub_arry ==<<>', sub_arry)

result = []

for i in sub_arry:
    result.append(sum(i))

print('result ==<<>>', result)