from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# ==========================================
# CONFIGURATION - Apni API Key yahan daalein
# ==========================================
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

messages = [{"role": "system", "content": "You are Garold AI. Creator: Aarav Kumar."}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global messages
    try:
        data = request.get_json()
        user_msg = data.get("message", "")
        if not user_msg: return jsonify({"reply": "No input"})

        img_keywords = ["generate image", "create image", "photo banao", "image banao"]
        is_image = any(k in user_msg.lower() for k in img_keywords)

        messages.append({"role": "user", "content": user_msg})
        
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=messages
        )
        ai_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_reply})

        return jsonify({"reply": ai_reply, "is_image": is_image})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    



    
    
