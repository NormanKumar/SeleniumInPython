numbers = []
for i in range(1,21):
    numbers.append(i)

evenNumbers = filter(lambda x: x % 2 == 0, numbers)
for(number) in evenNumbers:
    print(number)