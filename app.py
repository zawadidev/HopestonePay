from flask import Flask
import requests
import base64
import os

app = Flask(__name__)

# Get keys from environment (set these on Render)
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

# Function to generate M-Pesa access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(url, headers=headers)
    return response.json().get("access_token", "Error getting token")

# Home route
@app.route("/")
def home():
    return "HopestonePay backend is running!"

# Token route (for testing)
@app.route("/token")
def token():
    return get_access_token()

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
