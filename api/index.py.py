import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Render ke environment variables se API Key uthayega
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    if not OPENROUTER_API_KEY:
        return jsonify({"reply": "Error: API Key nahi mili. Render settings check karein."})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-2.0-flash-exp:free", # Ya jo model tum use kar rahe ho
        "messages": [
            {"role": "system", "content": "You are Garold AI, a helpful and witty assistant created by Aarav."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": f"Error: {response.status_code} - {response.text}"})
            
    except Exception as e:
        return jsonify({"reply": f"Bhai kuch gadbad ho gayi: {str(e)}"})

if __name__ == "__main__":
    # Render automatically port assign karta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
    



    
    
