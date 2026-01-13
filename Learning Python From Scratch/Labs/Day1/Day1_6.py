data = [1, 2, 3, 4, 5, 6, 2, 4]

squareData = []
for i in data:
    squareData.append(i**2)
print(squareData)

# 2. Set comprehension – unique even numbers
unique_evens = {x for x in data if x % 2 == 0}
print("Unique even numbers:", unique_evens)

# 3. Dictionary comprehension – number as key and its cube as value
cubes = {x: x**3 for x in data}
print("Number and its cube:", cubes)
