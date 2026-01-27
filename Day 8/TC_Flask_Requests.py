import requests

# url = "http://127.0.0.1:5000/users"
# response = requests.get(url)
# print(response.status_code)
# print(response.json())

# url1 = "http://127.0.0.1:5000/userid/2"
# response = requests.get(url1)
# print(response.status_code)
# print(response.json())

# url2 = "http://127.0.0.1:5000/users"
# body1 = {
#         "id": 4, "name": "Norman Kumar"
#     }
# response = requests.post(url2, json=body1)
# print(response.status_code)
# print(response.json())

url3 = "http://127.0.0.1:5000/users/2"
r = requests.post(url3)
print(r.status_code)
print(r.json())