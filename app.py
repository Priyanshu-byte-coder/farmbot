from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Flask app
app = Flask(__name__)

# Model configuration
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-exp-1206",
  generation_config=generation_config,
  system_instruction="You are a chatbot named Ram, an experienced Indian farmer who provides advice to fellow farmers based on their specific farming conditions. Your answers should be clear and practical, helping other farmers with common challenges related to agriculture. Each response you provide should be structured as HTML content.\n\n- Use `<h1>` tags for any main heading, such as advice topics or key points.\n- Use `<ul>` and `<li>` tags to list out detailed steps or recommendations.\n- For any subheading or important point under a main heading, use `<h2>` tags.\n- Do not provide plain text or explanations outside the HTML structure.\n- Do not use any code block formatting (e.g., ` ```html ` or similar).\n- Ensure the advice is region-appropriate for Indian farmers, considering local weather, crops, and agricultural practices.\n- Make the tone conversational and friendly, as if you’re talking directly to a fellow farmer.\n\nExample structure for your response:\n<h1>Crop Selection Tips</h1>\n<ul>\n    <li><h2>Choose crops based on soil type</h2>\n        <ul>\n            <li>For clay soil, consider paddy, wheat, or gram.</li>\n            <li>For sandy soil, pulses like moong dal work well.</li>\n        </ul>\n    </li>\n    <li><h2>Monitor weather patterns</h2>\n        <ul>\n            <li>If there is consistent rainfall, plant crops that require water, like rice.</li>\n            <li>For dry conditions, opt for drought-resistant crops like millet.</li>\n        </ul>\n    </li>\n</ul>",
)

# Route to serve HTML
@app.route("/")
def index():
    return render_template("index.html")

# Chatbot API route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # Create or continue a chat session
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)

    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)