import os
import sys
import time
from dotenv import load_dotenv
from web3 import Web3
from colorama import init, Fore, Style

# Initialize colors
init()

def print_info(msg):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")

def print_success(msg):
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")

def print_error(msg):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")

def main():
    print_info("Démarrage du Bot Polymarket...")
    
    # 1. Load Environment
    load_dotenv()
    rpc_url = os.getenv("POLYGON_RPC_URL")
    
    if not rpc_url:
        print_error("RPC URL manquante. Veuillez configurer le fichier .env")
        print_info("Copiez .env.example vers .env et ajoutez votre URL RPC.")
        return

    # 2. Connect to Polygon
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            print_success(f"Connecté à Polygon! Block actuel: {w3.eth.block_number}")
            
            # Check Gas Price
            gas_price = w3.eth.gas_price
            print_info(f"Gas Price actuel: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")
            
        else:
            print_error("Impossible de se connecter au RPC Polygon.")
    except Exception as e:
        print_error(f"Erreur de connexion: {str(e)}")

if __name__ == "__main__":
    main()
