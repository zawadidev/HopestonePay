from flask import Flask
import requests
import base64
import os

app = Flask(__name__)

# Get keys from environment (set these on Render)
CONSUMER_KEY = os.getenv"jAJ7Ud37RnflT0xAovWjaTwlKytCQ6r0F77bdCfNk5dYhkqI"
CONSUMER_SECRET = os.getenv"CUIchCcAb1EyqKGHLYhXJHCrsjDGml4qvVMr7d9uq33XKIfuS31YzYqILloKcJDQ"

# Function to generate M-Pesa access token
def get_access_token():
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        return "Error: Missing CONSUMER_KEY or CONSUMER_SECRET"

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers)

        return f"Status: {response.status_code}, Response: {response.text}"

    except Exception as e:
        return f"Server Error: {str(e)}"

# Home route
@app.route('/')
def home():
    return "HopestonePay API is running 🚀"

# Token route
@app.route('/token')
def token():
    return get_access_token()

# Run app
if __name__ == '__main__':
    app.run(debug=True)
