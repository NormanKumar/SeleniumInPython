data = [1, 2, 3, 4, 5, 6, 2, 4]

uniqueEvens = set()
for i in data:
    if i % 2 == 0:
        uniqueEvens.add(i)
print(uniqueEvens)