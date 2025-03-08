from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are 'Keshav', an AI assistant that provides insights from the Bhagavad Gita.
Answer all questions based on the Gita's teachings.
If the question is unrelated, politely refuse to answer.
"""

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"response": "Please ask a valid question."})

    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        reply = chat['choices'][0]['message']['content']
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
