from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Lấy API Key từ biến môi trường trên Render
API_KEY = os.environ.get("API_KEY", "sk-xt-4782187895af7e7cc0085d42b96eb7c5836fe08fc0310166")
XKIRO_API_URL = "https://api.xkiro.com/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if not API_KEY:
        return jsonify({"reply": "Lỗi: Bạn chưa cấu hình biến môi trường API_KEY trên Render!"})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",  # Bạn có thể đổi tên model nếu xKiro yêu cầu model khác
        "messages": [{"role": "user", "content": user_message}]
    }
    
    try:
        response = requests.post(XKIRO_API_URL, json=payload, headers=headers)
        
        # In kết quả ra Logs của Render để dễ dàng theo dõi khi lỗi
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            return jsonify({"reply": f"Lỗi từ xKiro (Mã {response.status_code}): {response.text}"})
            
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        return jsonify({"reply": f"Lỗi hệ thống: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
