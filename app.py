from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

# In-memory "database" (replace with real DB later)
users = {}
wallets = {}
transactions = []

# ------------------ AUTH ------------------

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

# ------------------ WALLET FEATURES ------------------

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))

    if phone not in wallets:
        return jsonify({"message": "User not found"}), 404

    wallets[phone]["balance"] += amount
    wallets[phone]["points"] += int(amount // 100)

    transactions.append({
        "type": "deposit",
        "user": phone,
        "amount": amount,
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({"message": "Deposit successful", "wallet": wallets[phone]})

@app.route("/send-money", methods=["POST"])
def send_money():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = float(data.get("amount"))

    if sender not in wallets or receiver not in wallets:
        return jsonify({"message": "Sender or receiver not found"}), 404

    if wallets[sender]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400

    fee = amount * 0.02
    savings_share = fee / 2

    wallets[sender]["balance"] -= amount
    wallets[receiver]["balance"] += amount - fee
    wallets[sender]["savings"] += savings_share
    wallets[sender]["points"] += int(amount // 100)

    transactions.append({
        "type": "send",
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "fee": fee,
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({"message": "Transaction successful", "wallet": wallets[sender]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))

    if wallets[phone]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400

    wallets[phone]["balance"] -= amount

    transactions.append({
        "type": "withdraw",
        "user": phone,
        "amount": amount,
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({"message": "Withdraw successful", "wallet": wallets[phone]})

@app.route("/airtime", methods=["POST"])
def airtime():
    data = request.json
    phone = data.get("phone")
    amount = float(data.get("amount"))

    if wallets[phone]["balance"] < amount:
        return jsonify({"message": "Insufficient funds"}), 400

    wallets[phone]["balance"] -= amount
    wallets[phone]["points"] += int(amount // 50)

    transactions.append({
        "type": "airtime",
        "user": phone,
        "amount": amount,
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({"message": "Airtime purchase successful", "wallet": wallets[phone]})

@app.route("/withdraw-savings", methods=["POST"])
def withdraw_savings():
    data = request.json
    phone = data.get("phone")

    if wallets[phone]["savings"] >= 5000:
        wallets[phone]["balance"] += wallets[phone]["savings"]
        wallets[phone]["savings"] = 0
        transactions.append({
            "type": "savings-withdraw",
            "user": phone,
            "timestamp": datetime.datetime.now().isoformat()
        })
        return jsonify({"message": "Savings withdrawn", "wallet": wallets[phone]})
    else:
        return jsonify({"message": "Savings below withdrawal threshold", "wallet": wallets[phone]})

@app.route("/transactions", methods=["GET"])
def get_transactions():
    return jsonify({"transactions": transactions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
