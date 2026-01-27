import requests

url = "https://api.restful-api.dev/objects"
response = requests.get(url)

print(response.status_code)
print(response.json())

posturl = "https://api.restful-api.dev/objects"
body1={
   "name": "Apple MacBook Pro 16",
   "data": {
      "year": 2019,
      "price": 1849.99,
      "CPU model": "Intel Core i9",
      "Hard disk size": "1 TB"
   }
}
r1 = requests.post(posturl, json=body1)
print(r1.status_code)
print(r1.json())