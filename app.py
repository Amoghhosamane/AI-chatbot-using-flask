from flask import Flask, render_template, request, jsonify
from chatbot_engine import ChatbotEngine

app = Flask(__name__)

# Initialize the chatbot engine
engine = ChatbotEngine()
engine.load_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_text = request.json.get("message")
    user_id = request.json.get("userID", "123")
    
    if not user_text:
        return jsonify({"response": "I didn't hear anything!"})
        
    bot_response = engine.get_response(user_text, userID=user_id)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
