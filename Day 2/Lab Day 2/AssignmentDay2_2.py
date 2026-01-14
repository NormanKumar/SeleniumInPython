def fibonacci(n):
    a = 0
    b = 1
    i = 0
    while i < n:
        yield a
        temp = a
        a = b
        b = temp + b
        i += 1

for i in fibonacci(5):
    print(i)