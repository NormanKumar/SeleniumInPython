def numbers():
    yield 1
    yield 2
    yield 3

gen = numbers()
print(next(gen))
print(next(gen))
print(next(gen))

def count_up(n):
    for i in range(n):
        yield i
for val in count_up(5):
    print(val)