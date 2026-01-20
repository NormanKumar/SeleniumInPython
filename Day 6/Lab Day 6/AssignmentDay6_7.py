import re

text = "Python"
print(bool(re.search("python", text)))
print(bool(re.search("python", text, re.IGNORECASE)))

text = "apple\nbanana\ncherry"
pattern = r'^banana'
print(re.findall(pattern, text))
print(re.findall(pattern, text, re.MULTILINE))

text = "Hello\nWorld"
print(re.search(r'Hello.*World', text))
print(bool(re.search(r'Hello.*World', text, re.DOTALL)))

