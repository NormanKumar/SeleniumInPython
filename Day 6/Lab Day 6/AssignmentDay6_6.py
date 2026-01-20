import re

def validate_password(password):
    pattern = (
        r'^(?=.*[A-Z])'      
        r'(?=.*[a-z])'       
        r'(?=.*\d)'          
        r'(?=.*[@$!%*?&])'   
        r'.{8,}$'
    )

    return bool(re.search(
        pattern,
        password,
        re.IGNORECASE | re.DOTALL
    ))

pwd = input("Enter password: ")
print("Valid password" if validate_password(pwd) else "Invalid password")

