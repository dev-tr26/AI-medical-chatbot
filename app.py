from flask import Flask, request, redirect,render_template
from flask import jsonify , session
from src.prompt import *
from chat_feature.chat_service import get_response, clear_session_cache, get_recent_history
import uuid


app =Flask(__name__)
app.secret_key = "some_secret_key"


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4)
    return render_template("chatbot.html")


@app.route("/llm_chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message")

    if not session_id or not user_message:
        return jsonify({"error": "Missing session_id or message"}), 400

    bot_response = get_response(session_id, user_message)
    return jsonify({"response": bot_response})

    
@app.route('/clear_chat/<session_id>', methods=['POST'])
def clear_session(session_id):
    clear_session_cache(session_id)
    return jsonify({"message": f"Session {session_id} cleared."})


@app.route('/history/<session_id>', methods=['GET'])
def history(session_id):
    history = get_recent_history(session_id)
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)


# if __name__ == '__main__':
    # app.run(host="0.0.0.0", port= 8080, debug= True)