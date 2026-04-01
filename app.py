from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # allow frontend requests

# In-memory "database"
users = {}
wallets = {}
transactions = []

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    phone = data.get("phone")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if phone in users:
        return jsonify({"message": "User already exists"}), 400

    password_hash = generate_password_hash(password)
    users[phone] = {"name": name, "email": email, "password_hash": password_hash}
    wallets[phone] = {"balance": 0, "savings": 0, "points": 0}

    return jsonify({"message": "Registration successful"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    phone = data.get("phone")
    password = data.get("password")

    user = users.get(phone)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "wallet": wallets[phone]})

# Example wallet actions (deposit, withdraw, send, airtime)
@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))
    wallets[phone]["balance"] += amount
    return jsonify({"message": "Deposit successful", "wallet": wallets[phone]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))
    if wallets[phone]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400
    wallets[phone]["balance"] -= amount
    return jsonify({"message": "Withdraw successful", "wallet": wallets[phone]})

@app.route("/send-money", methods=["POST"])
def send_money():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = float(data.get("amount"))
    if wallets[sender]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400
    wallets[sender]["balance"] -= amount
    wallets[receiver]["balance"] += amount
    return jsonify({"message": "Transaction successful"})

@app.route("/airtime", methods=["POST"])
def airtime():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))
    if wallets[phone]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400
    wallets[phone]["balance"] -= amount
    return jsonify({"message": "Airtime purchase successful", "wallet": wallets[phone]})

if __name__ == "__main__":
    # Pre-register admin user
    admin_phone = "0799558414"
    admin_password = "1234"
    users[admin_phone] = {
        "name": "Samuel Ouma",
        "email": "cochsam3@gmail.com",
        "password_hash": generate_password_hash(admin_password)
    }
    wallets[admin_phone] = {"balance": 0, "savings": 0, "points": 0}
    app.run(host="0.0.0.0", port=10000)
