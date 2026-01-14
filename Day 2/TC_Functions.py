def add(a,b):
    return a+b

def subtract(a,b):
    return a-b,a,b # Returns as a tuple

def hello(greeting: "Hello", name="Harish"):
    print('%s,%s'%(greeting,name))

def print_param(*params):
    print(params)

def print_param1(**params):
    print(params)

print(add(10,20))
print(subtract(20,10))
hello("Welcome")
print_param('Testing')
print_param(1,2,3,4)
print_param1(x = 1,y =2, z = 3)