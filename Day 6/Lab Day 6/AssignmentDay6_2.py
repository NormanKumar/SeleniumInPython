import re

def validEmailID(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else None

text1 = "My email id is 2105RahulKumar@gmail.com"
text2 = "Hi my name is Rahul"

print(validEmailID(text1))
print(validEmailID(text2))

