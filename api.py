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

@app.route('/api/config/toggle-mode', methods=['POST'])
def toggle_trading_mode():
    from flask import request
    import re
    
    data = request.json
    paper_trading = data.get('paper_trading', True)
    
    config_path = 'config.py'
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Update PAPER_TRADING value
        content = re.sub(r'PAPER_TRADING = (True|False)', f'PAPER_TRADING = {paper_trading}', content)
        
        with open(config_path, 'w') as f:
            f.write(content)
        
        mode = "Paper Trading" if paper_trading else "Real Trading"
        return jsonify({"status": "success", "message": f"Mode changé: {mode}. Redémarrez le bot."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/opportunities')
def get_opportunities():
    if os.path.exists('opportunities.json'):
        with open('opportunities.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify({"trending": [], "price_movements": [], "keywords": []})

@app.route('/api/whitelist', methods=['GET'])
def get_whitelist():
    if os.path.exists('whitelist.json'):
        with open('whitelist.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/whitelist', methods=['POST'])
def add_whitelist():
    from flask import request
    data = request.json
    address = data.get('address')
    if not address:
        return jsonify({"status": "error", "message": "Address required"}), 400
    
    whitelist = []
    if os.path.exists('whitelist.json'):
        with open('whitelist.json', 'r') as f:
            whitelist = json.load(f)
    
    if address not in whitelist:
        whitelist.append(address)
        with open('whitelist.json', 'w') as f:
            json.dump(whitelist, f)
            
    return jsonify({"status": "success", "whitelist": whitelist})

@app.route('/api/whitelist', methods=['DELETE'])
def remove_whitelist():
    from flask import request
    data = request.json
    address = data.get('address')
    
    whitelist = []
    if os.path.exists('whitelist.json'):
        with open('whitelist.json', 'r') as f:
            whitelist = json.load(f)
            
    if address in whitelist:
        whitelist.remove(address)
        with open('whitelist.json', 'w') as f:
            json.dump(whitelist, f)
            
    return jsonify({"status": "success", "whitelist": whitelist})

@app.route('/api/config/wallet', methods=['POST'])
def save_wallet():
    from flask import request
    import re
    
    data = request.json
    private_key = data.get('private_key', '').strip()
    
    if not private_key:
        return jsonify({"status": "error", "message": "Private key required"}), 400
    
    # Basic validation (should start with 0x and be 66 chars)
    if not private_key.startswith('0x') or len(private_key) != 66:
        return jsonify({"status": "error", "message": "Invalid private key format"}), 400
    
    env_path = '.env'
    
    try:
        # Read or create .env
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        # Update or add PRIVATE_KEY
        if 'PRIVATE_KEY=' in content:
            content = re.sub(r'PRIVATE_KEY=.*', f'PRIVATE_KEY={private_key}', content)
        else:
            content += f'\nPRIVATE_KEY={private_key}\n'
        
        # Write back
        with open(env_path, 'w') as f:
            f.write(content)
        
        return jsonify({"status": "success", "message": "Wallet configured. Restart bot to apply."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Dashboard API on http://localhost:5000")
    app.run(debug=True, port=5000)
