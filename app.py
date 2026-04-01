from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Example in-memory "database" (replace with real DB later)
users = {}
wallets = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    phone = data.get("phone")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if phone in users:
        return jsonify({"message": "User already exists"}), 400

    # Hash password for security
    password_hash = generate_password_hash(password)

    # Save user
    users[phone] = {
        "name": name,
        "email": email,
        "password_hash": password_hash
    }

    # Create wallet
    wallets[phone] = {"balance": 0, "savings": 0, "points": 0}

    return jsonify({"message": "Registration successful", "user": users[phone]})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    phone = data.get("phone")
    password = data.get("password")

    user = users.get(phone)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "wallet": wallets[phone]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
