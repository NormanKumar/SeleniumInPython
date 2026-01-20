import re

def strong_password(password):
    pattern = (
        r'^(?=.*[A-Z])'      
        r'(?=.*[a-z])'       
        r'(?=.*\d)'          
        r'(?=.*[@$!%*?&])'   
        r'[A-Za-z\d@$!%*?&]{8,}$'
    )
    return bool(re.match(pattern, password, re.ASCII))

password = input("Enter password: ")
if strong_password(password):
    print("Strong password")
else:
    print("Weak password")
