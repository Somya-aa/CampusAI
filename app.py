import os

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
app.secret_key = "campusai-secret-key"

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question")

    conversation = session.get("conversation", [])

    conversation.append({
    "role": "user",
    "parts": [
        {"text": question}
        ]
    })

    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=conversation
    )

    except Exception as e:
        print("Gemini Error:", e)

        return jsonify({
           "answer": "Sorry, I'm temporarily unavailable. Please try again."
        })
    

    conversation.append({
    "role": "model",
    "parts": [
        {"text": response.text}
        ]
    })

    session["conversation"] = conversation

    return jsonify({
        "answer": response.text
    })

@app.route("/clear", methods=["POST"])
def clear_chat():

    session.pop("conversation", None)

    return jsonify({
        "message": "Chat cleared"
    })


if __name__ == "__main__":
    app.run(debug=True)