from flask import Flask, render_template, request, jsonify
from g4f.client import Client
import os

app = Flask(__name__)
client = Client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message.strip():
        return jsonify({"reply": "Vui lòng nhập tin nhắn!"})
    
    try:
        # Gọi AI miễn phí qua g4f
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"reply": f"Xin lỗi, hiện tại hệ thống AI đang bận. Bạn thử lại sau nhé! (Lỗi: {str(e)})"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
