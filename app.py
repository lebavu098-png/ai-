from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Lấy API Key từ biến môi trường của Render hoặc điền trực tiếp khi test ở máy
API_KEY = os.environ.get("API_KEY", "sk-xt-4782187895af7e7cc0085d42b96eb7c5836fe08fc0310166")
XKIRO_API_URL = "https://api.xkiro.com/v1/chat/completions"  # Đường dẫn API chuẩn của xKiro

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "gpt-3.5-turbo", # Hoặc tên model mà xKiro hỗ trợ
        "messages": [{"role": "user", "content": user_message}]
    }
    
    try:
        response = requests.post(XKIRO_API_URL, json=payload, headers=headers)
        data = response.json()
        
        # Trích xuất câu trả lời từ chuẩn OpenAI/xKiro format
        bot_reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Lỗi kết nối API: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
