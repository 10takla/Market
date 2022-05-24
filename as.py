arr = []


for i in range(2):
    r = []
    for j in range(5):
        r.append(j+i*5)
    arr.append(r)
print(arr)
print(arr[1][3])