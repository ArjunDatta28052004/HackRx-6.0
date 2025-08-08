from flask import Flask, request, jsonify
from main import process_insurance_query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/process_query", methods=["POST"])
def process_query():
    try:
        data = request.get_json()
        user_text = data.get("query", "")
        result = process_insurance_query(user_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
