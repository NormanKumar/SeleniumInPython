import re

def findFirstEmail(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else None

text1 = "Please contact us at support@gmail.com for help."
text2 = "No email address here!"

print(findFirstEmail(text1))
print(findFirstEmail(text2))

