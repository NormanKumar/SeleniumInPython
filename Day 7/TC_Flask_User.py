from flask import Flask,request, jsonify
app = Flask(__name__)

users=[{
    "id": 1,
    "name": "Norman",
},
    {
        "id": 2,
        "name": "Harsh",
    }]
@app.route("/",methods=['GET'])
def home():
    return "Welcome to Flask"

@app.route("/users",methods=['GET'])
def get_users():
    return jsonify(users)

@app.route("/userid/<int:user_id>",methods=['GET'])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"message": "User does not exist"}),404


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    newuser = {
        "id": len(users) + 1, "name": data.get("name")
    }
    users.append(newuser)
    return jsonify(newuser), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name")
            return jsonify(user)
    return jsonify({"message": "user not found"}), 404
#
# @app.route("/users/<int:user_id>", methods=["PATCH"])
# def update_user(user_id):
#     data = request.json
#     for user in users:
#         if user["id"] == user_id:
#             user["name"] = data.get("name")
#             return jsonify(user)
#     return jsonify({"message": "user not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)



