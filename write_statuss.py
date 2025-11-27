from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrapper_status.txt")


@app.route("/webhook/scrapper_status", methods=["POST"])
def scrapper_status():
    """
    Receives data from the webhook and persists the payload to scrapper_status.txt.
    Falls back to the raw body if the request is not valid JSON.
    """
    json_payload = request.get_json(silent=True)
    payload_text = json.dumps(json_payload, ensure_ascii=False) if json_payload is not None else request.get_data(as_text=True)

    # Ensure we always write something for traceability
    payload_to_write = payload_text if payload_text else ""
    with open(STATUS_FILE, "w", encoding="utf-8") as status_file:
        status_file.write(payload_to_write)

    return jsonify({"status": "received", "data": json_payload if json_payload is not None else payload_to_write}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    # Optionally define DEBUG (set to False by default)
    DEBUG = bool(os.environ.get("DEBUG", False))
    app.run(host="0.0.0.0", port=port, debug=DEBUG)