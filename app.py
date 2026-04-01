from flask import Flask, request, jsonify

app = Flask(__name__)

# Example wallets (replace with database later)
wallets = {
    "user1": {"balance": 1000, "savings": 0},
    "user2": {"balance": 500, "savings": 0},
}
company = {"revenue": 0}

@app.route("/")
def home():
    return "HopestonePay backend is running!"

@app.route("/send-money", methods=["POST"])
def send_money():
    data = request.json
    sender = data["sender"]
    receiver = data["receiver"]
    amount = float(data["amount"])

    # Transaction fee (2%)
    fee = amount * 0.02
    company_share = fee / 2
    savings_share = fee / 2

    # Deduct from sender
    wallets[sender]["balance"] -= amount

    # Credit receiver (minus fee)
    wallets[receiver]["balance"] += amount - fee

    # Company revenue
    company["revenue"] += company_share

    # Add to sender’s savings
    wallets[sender]["savings"] += savings_share

    return jsonify({
        "message": "Transaction successful",
        "fee": fee,
        "company_share": company_share,
        "savings_added": savings_share,
        "sender_wallet": wallets[sender],
        "receiver_wallet": wallets[receiver]
    })

@app.route("/withdraw-savings", methods=["POST"])
def withdraw_savings():
    data = request.json
    user = data["user"]

    if wallets[user]["savings"] >= 5000:
        wallets[user]["balance"] += wallets[user]["savings"]
        wallets[user]["savings"] = 0
        return jsonify({"message": "Savings withdrawn", "wallet": wallets[user]})
    else:
        return jsonify({"message": "Savings below withdrawal threshold", "wallet": wallets[user]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
