import re

def validEmployeeID(s):
    pattern = r'^EMP\d{3}'
    return bool(re.match(pattern, s))

print(validEmployeeID("EMP123 Rohit Sharma"))
print(validEmployeeID("EMP12 Rohit Sharma"))
print(validEmployeeID("ABCEMP123"))
