from flask import Flask, render_template, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Lỗi: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
