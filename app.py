from flask import Flask, render_template, request, jsonify
import google.generativeai as genai


app = Flask(__name__, template_folder='templates')

client = genai.Client(api_key="AIzaSyAayceWjtN_ZGB5kJeGSVw6_zCamnX1U-w")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message
        )
        if hasattr(response, 'text'):
            clean_text = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            clean_text = response.candidates[0].content.parts[0].text.strip()
        else:
            clean_text = "Sorry, I couldn't understand the response."
        return jsonify({"response": clean_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
