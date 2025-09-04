from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os   # ✅ for environment variable

app = Flask(__name__)
CORS(app)

# ✅ Get API Key from environment variable (set in Render dashboard)
API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload)
        data = response.json()

        # Debug print
        print("=== Gemini Raw Response ===")
        print(data)

        # Extract reply
        if "candidates" in data and len(data["candidates"]) > 0:
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                bot_reply = parts[0]["text"]
            else:
                bot_reply = "⚠️ No text found in response."
        else:
            bot_reply = "⚠️ No candidates returned."

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"❌ Error: {str(e)}"})


# ✅ Remove debug=True (Render doesn’t need it)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
