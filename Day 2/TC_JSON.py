import json
data={
    "name":"Bob",
    "age":20,
    "salary":20000
}
with open('data.json', 'w') as file:
    json.dump(data, file,indent=4)