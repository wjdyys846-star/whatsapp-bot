from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "12345"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
    data = request.get_json()
    print(data)
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"]
        url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        payload = {"messaging_product": "whatsapp", "to": sender, "text": {"body": f"وصلتني رسالتك: {text}"}}
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
