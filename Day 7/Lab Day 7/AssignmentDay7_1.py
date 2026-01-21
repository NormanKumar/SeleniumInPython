from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users[user_id]), 200

@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json(silent=True)

    if not data or "name" not in data or not data["name"].strip():
        return jsonify({"error": "Name is required"}), 400

    new_id = max(users.keys()) + 1 if users else 1

    new_user = {
        "id": new_id,
        "name": data["name"]
    }
    users[new_id] = new_user
    return jsonify(new_user), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
