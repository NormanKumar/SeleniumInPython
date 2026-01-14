from functools import reduce

numbers = []
for i in range(1,21):
    numbers.append(i)

evenNumbers = filter(lambda x: x % 2 == 0, numbers)
squaredEvens = map(lambda x: x * x, evenNumbers)
sumOfSquares = reduce(lambda a, b: a + b, squaredEvens)
print(sumOfSquares)

