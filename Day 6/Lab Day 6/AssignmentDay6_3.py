import re

text = "Employee EMP123 works in IT"

pattern = r'Employee\s+(\w+)\d+.*?works\s+in\s+(\w+)'
match = re.search(pattern, text)

if match:
    print("Full match:", match.group(0))
    print("Employee prefix:", match.group(1))
    print("Department:", match.group(2))
