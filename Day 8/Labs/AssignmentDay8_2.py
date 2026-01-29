import requests, json

public_api_url = "https://jsonplaceholder.typicode.com/users"

customHeader = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Python-Requests-Client"
}

user_data = requests.get(public_api_url, customHeader)
print(user_data.status_code)
response_data = user_data.json()
print(response_data)
print("\n")
print(response_data[1])
try:
    with open("userdump.json", 'w') as file:
        json.dump(response_data, file, indent=4)

except Exception as e:
    print(f"error dumping data into file: {str(e)}")
