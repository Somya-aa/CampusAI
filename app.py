import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=question
    )

    return jsonify({
        "answer": response.text
    })


if __name__ == "__main__":
    app.run(debug=True)