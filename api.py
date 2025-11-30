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

@app.route('/api/config')
def get_config():
    import config
    return jsonify({
        "paper_trading": config.PAPER_TRADING,
        "max_position_size": config.MAX_POSITION_SIZE_USD,
        "stop_loss": config.STOP_LOSS_PERCENT,
        "take_profit": config.TAKE_PROFIT_PERCENT,
        "max_positions": config.MAX_OPEN_POSITIONS,
        "min_whale_score": config.MIN_WHALE_SCORE,
        "scan_interval": config.SCAN_INTERVAL
    })

@app.route('/api/config/save', methods=['POST'])
def save_config():
    from flask import request
    import re
    
    data = request.json
    config_path = 'config.py'
    
    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Update values
        content = re.sub(r'MAX_POSITION_SIZE_USD = [\d.]+', f'MAX_POSITION_SIZE_USD = {data["max_position_size"]}', content)
        content = re.sub(r'STOP_LOSS_PERCENT = [\d.]+', f'STOP_LOSS_PERCENT = {data["stop_loss"]}', content)
        content = re.sub(r'TAKE_PROFIT_PERCENT = [\d.]+', f'TAKE_PROFIT_PERCENT = {data["take_profit"]}', content)
        content = re.sub(r'MAX_OPEN_POSITIONS = \d+', f'MAX_OPEN_POSITIONS = {data["max_positions"]}', content)
        content = re.sub(r'MIN_WHALE_SCORE = \d+', f'MIN_WHALE_SCORE = {data["min_whale_score"]}', content)
        content = re.sub(r'SCAN_INTERVAL = \d+', f'SCAN_INTERVAL = {data["scan_interval"]}', content)
        
        # Write back
        with open(config_path, 'w') as f:
            f.write(content)
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Dashboard API on http://localhost:5000")
    app.run(debug=True, port=5000)
