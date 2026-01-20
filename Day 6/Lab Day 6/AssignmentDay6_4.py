import re

text = "Employee ID: EMP123"

pattern = r'Employee ID:\s+(EMP(\d{3}))'
match = re.search(pattern, text)

if match:
    print("Employee ID:", match.group(1))
    print("Employee Number:", match.group(2))
