from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Norman"},
    2: {"id": 2, "name": "Harsh"}
}

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id]), 200

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_id = len(users) + 1
    newuser = {
        "id": new_id,
        "name": data.get("name")
    }
    users[new_id] = newuser  # Fixed: Add to dictionary instead of append
    return jsonify(newuser), 201

if __name__ == '__main__':
    app.run(debug=True)