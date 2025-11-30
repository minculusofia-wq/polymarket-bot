from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='dashboard')
CORS(app)

WHALES_FILE = "whales.json"
HISTORY_FILE = "trade_history.json"

@app.route('/')
def index():
    return send_from_directory('dashboard', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('dashboard', path)

@app.route('/api/whales')
def get_whales():
    if os.path.exists(WHALES_FILE):
        with open(WHALES_FILE, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/history')
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/status')
def get_status():
    return jsonify({"status": "running", "mode": "paper_trading"})

if __name__ == '__main__':
    print("Starting Dashboard API on http://localhost:5000")
    app.run(debug=True, port=5000)
