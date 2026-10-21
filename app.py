from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Thay thế bằng API Key thực tế của bạn
API_KEY = "sk-xt-a98d4d8eb8c587537c9f84c47d5c1eb21db1af58cfa31e25"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    # Gửi yêu cầu đến Gemini API
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        data = response.json()
        
        # Trích xuất câu trả lời từ AI
        bot_reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "Xin lỗi, đã có lỗi xảy ra hoặc API Key chưa chính xác."})

if __name__ == "__main__":
    app.run(debug=True)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)