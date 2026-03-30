import requests
import base64
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# ====== YOUR DETAILS (REPLACE THESE) ======
CONSUMER_KEY = "jAJ7Ud37RnflT0xAovWjaTwlKytCQ6r0F77bdCfNk5dYhkqI"
CONSUMER_SECRET = "CUIchCcAb1EyqKGHLYhXJHCrsjDGml4qvVMr7d9uq33XKIfuS31YzYqILloKcJDQ"
SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
PHONE = "254799558414"
AMOUNT = 1

# 🔥 IMPORTANT: PUT YOUR NGROK LINK HERE
CALLBACK_URL = "https://abcd1234.ngrok-free.app/callback"


# ====== GET ACCESS TOKEN ======
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Failed to get access token")
        return None


# ====== STK PUSH ======
def stk_push():
    access_token = get_access_token()

    if not access_token:
        return

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": AMOUNT,
        "PartyA": PHONE,
        "PartyB": SHORTCODE,
        "PhoneNumber": PHONE,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "HopestonePay",
        "TransactionDesc": "Test Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STK STATUS:", response.status_code)
    print("STK RESPONSE:", response.text)

    if response.status_code == 200:
        print("✅ Payment request sent successfully!")
    else:
        print("❌ Payment failed!")


# ====== CALLBACK ROUTE ======
@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    print("📩 CALLBACK RECEIVED:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


# ====== HOME ======
@app.route('/')
def home():
    return '''
    <h2>💰 HopestonePay</h2>

    <form action="/pay" method="get">
        <input type="text" placeholder="Phone Number" required><br><br>
        <input type="number" placeholder="Amount" required><br><br>
        <button type="submit">Send Money 🚀</button>
    </form>
    '''

# 👉 ADD IT HERE 👇
@app.route('/pay')
def pay():
    stk_push()
    return "Payment request sent 🚀"

# ====== RUN ======
if __name__ == "__main__":
    app.run(port=5000)


# ====== RUN ======
if __name__ == "__main__":
    stk_push()
    app.run(port=5000)