from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["company_db"]
collection = db["employees"]

collection.insert_one({
    "name": "Amit",
    "department": "IT",
    "salary": 55000
})

for emp in collection.find({"department": "IT"}):
    print(emp)

collection.update_one(
    {"name": "Amit"},
    {"$set": {"salary": 60000}}
)
