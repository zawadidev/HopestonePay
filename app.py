from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend running"

@app.route("/register", methods=["POST"])
def register():
    return jsonify({"message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Login successful"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
