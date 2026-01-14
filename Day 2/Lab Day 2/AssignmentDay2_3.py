# Iterator
class count:
    def __init__(self, n):
        self.n = n
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.n:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration

it = count(5)
for i in it:
    print(i)

# Generator
def count(n):
    for i in range(1, n + 1):
        yield i

for i in count(5):
    print(i)
