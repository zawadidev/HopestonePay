from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = {}
transactions = {}

# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users:
        return jsonify({"error": "User already exists"})

    users[username] = {
        "password": password,
        "balance": 0,
        "savings": 0,
        "points": 0
    }
    transactions[username] = []

    return jsonify({"message": "User registered successfully"})


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users and users[username]["password"] == password:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"})


# Get dashboard data
@app.route("/dashboard/<username>")
def dashboard(username):
    user = users.get(username)
    return jsonify({
        "balance": user["balance"],
        "savings": user["savings"],
        "points": user["points"],
        "transactions": transactions[username]
    })


# Deposit
@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    u = users[data["username"]]
    amount = int(data["amount"])

    u["balance"] += amount
    u["points"] += amount // 10
    transactions[data["username"]].append(f"Deposited {amount}")

    return jsonify({"message": "Deposit successful"})


# Send
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    sender = users[data["from"]]
    receiver = users.get(data["to"])
    amount = int(data["amount"])

    if not receiver:
        return jsonify({"error": "User not found"})

    if sender["balance"] < amount:
        return jsonify({"error": "Insufficient balance"})

    sender["balance"] -= amount
    receiver["balance"] += amount

    transactions[data["from"]].append(f"Sent {amount} to {data['to']}")
    transactions[data["to"]].append(f"Received {amount} from {data['from']}")

    return jsonify({"message": "Sent successfully"})


# Withdraw
@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    u = users[data["username"]]
    amount = int(data["amount"])

    if u["balance"] < amount:
        return jsonify({"error": "Insufficient balance"})

    u["balance"] -= amount
    transactions[data["username"]].append(f"Withdrew {amount}")

    return jsonify({"message": "Withdraw successful"})


# Airtime
@app.route("/airtime", methods=["POST"])
def airtime():
    data = request.json
    u = users[data["username"]]
    amount = int(data["amount"])

    if u["balance"] < amount:
        return jsonify({"error": "Insufficient balance"})

    u["balance"] -= amount
    transactions[data["username"]].append(f"Airtime {amount}")

    return jsonify({"message": "Airtime purchased"})


# Save money
@app.route("/save", methods=["POST"])
def save():
    data = request.json
    u = users[data["username"]]
    amount = int(data["amount"])

    if u["balance"] < amount:
        return jsonify({"error": "Not enough balance"})

    u["balance"] -= amount
    u["savings"] += amount

    transactions[data["username"]].append(f"Saved {amount}")

    return jsonify({"message": "Saved successfully"})


# Withdraw savings (locked until 5000)
@app.route("/withdraw_savings", methods=["POST"])
def withdraw_savings():
    data = request.json
    u = users[data["username"]]

    if u["savings"] < 5000:
        return jsonify({"error": "Savings locked until 5000 KSH"})

    u["balance"] += u["savings"]
    u["savings"] = 0

    return jsonify({"message": "Savings withdrawn"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
