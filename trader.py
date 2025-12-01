import time
import json
import os
from datetime import datetime
import config

class Trader:
    def __init__(self):
        self.paper_trading = config.PAPER_TRADING
        self.positions = {}
        self.balance = 1000.0 if self.paper_trading else 0.0 # Mock balance for paper trading
        self.history_file = "trade_history.json"
        self.load_history()
        
        if self.paper_trading:
            print(f"--- TRADER INITIALIZED (PAPER TRADING) ---")
            print(f"Initial Balance: ${self.balance}")
        else:
            print(f"--- TRADER INITIALIZED (REAL TRADING) ---")
            # TODO: Fetch real balance from chain

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.positions = data.get('positions', {})
                    self.balance = data.get('balance', self.balance)
            except:
                pass

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump({
                "positions": self.positions,
                "balance": self.balance,
                "last_update": datetime.now().isoformat()
            }, f, indent=2)

    def execute_copy_trade(self, whale_address, market_id, outcome, amount_usd):
        """
        Execute a trade copying a whale.
        """
        if len(self.positions) >= config.MAX_OPEN_POSITIONS:
            print(f"Skipping trade: Max open positions reached ({config.MAX_OPEN_POSITIONS})")
            return

        # Risk Check
        amount = min(amount_usd, config.MAX_POSITION_SIZE_USD)
        
        if self.paper_trading:
            self._paper_trade(whale_address, market_id, outcome, amount)
        else:
            self._real_trade(whale_address, market_id, outcome, amount)

    def _paper_trade(self, whale_address, market_id, outcome, amount):
        print(f"PAPER TRADE: Buying ${amount} of {outcome} in market {market_id} (Copying {whale_address[:10]}...)")
        
        # Simulate execution
        entry_price = 0.50 # Mock price, ideally fetch from CLOB
        shares = amount / entry_price
        
        position_id = f"{market_id}_{outcome}_{int(time.time())}"
        self.positions[position_id] = {
            "market_id": market_id,
            "outcome": outcome,
            "entry_price": entry_price,
            "shares": shares,
            "amount_invested": amount,
            "timestamp": datetime.now().isoformat(),
            "whale": whale_address,
            "status": "OPEN"
        }
        
        self.balance -= amount
        self.save_history()
        print(f"Trade Executed. New Balance: ${self.balance:.2f}")

    def _real_trade(self, whale_address, market_id, outcome, amount):
        print("REAL TRADING NOT YET IMPLEMENTED - SAFETY LOCK ENGAGED")
        pass

    def check_positions(self):
        """
        Monitor open positions for stop loss / take profit.
        """
        print(f"Checking {len(self.positions)} open positions...")
        # In a real scenario, we would fetch current prices here.
        # For paper trading, we can simulate price movement or just print status.
        pass

    def liquidate_position(self, position_id, reason="Manual"):
        """
        Liquidate a specific position.
        """
        if position_id not in self.positions:
            print(f"Error: Position {position_id} not found.")
            return False
            
        position = self.positions[position_id]
        if position['status'] != 'OPEN':
            print(f"Position {position_id} is already {position['status']}")
            return False
            
        print(f"LIQUIDATING Position {position_id} ({reason})...")
        
        # Calculate P&L (Mock for paper trading)
        # In real trading, fetch current price
        exit_price = position['entry_price'] * 1.05 # Mock 5% profit
        
        if self.paper_trading:
            proceeds = position['shares'] * exit_price
            self.balance += proceeds
            
            # Update position
            self.positions[position_id]['status'] = 'CLOSED'
            self.positions[position_id]['exit_price'] = exit_price
            self.positions[position_id]['exit_timestamp'] = datetime.now().isoformat()
            self.positions[position_id]['pnl'] = proceeds - position['amount_invested']
            self.positions[position_id]['exit_reason'] = reason
            
            self.save_history()
            print(f"Position Liquidated. P&L: ${self.positions[position_id]['pnl']:.2f}. New Balance: ${self.balance:.2f}")
            return True
        else:
            print("REAL TRADING LIQUIDATION NOT YET IMPLEMENTED")
            return False
