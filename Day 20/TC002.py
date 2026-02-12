from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["Company_db"]
collection = db["C1"]

# insert document
# result = collection.insert_one({
#     "name": "Harsh",
#     "dep": "CSE",
#     "course": "Java",
#     "salary": 10000
# })
#
# print("Inserted ID:", result.inserted_id)

# fetch document
result1 = collection.find_one({"name": "Norman Kumar"})
print("Fetched record:", result1)
