# Polymarket Bot

Un bot de trading automatisé pour Polymarket qui identifie et suit les "whales" (gros traders) en analysant leurs activités de trading.

## 🎯 Fonctionnalités

### ✅ Phase 1 : Infrastructure
- Connexion à la blockchain Polygon
- Configuration de l'environnement Python
- Gestion sécurisée des clés via `.env`

### ✅ Phase 2 : Scanner de Whales
- **Analyse des trades récents** via l'API Polymarket
- **Identification des top traders** par volume
- **Tracking des wallets actifs** avec historique
- **Export des données** en JSON

### ✅ Phase 3 : Scanner Amélioré
- **Scoring des Whales** : Win rate, ROI, Consistance
- **Monitoring Continu** : Scan toutes les 60 secondes
- **Tracking des Positions** : Suivi des positions ouvertes

### ✅ Phase 4 : Copy-Trading (Paper Trading)
- **Exécution Automatique** : Copie les trades des top whales
- **Gestion des Risques** : Stop loss, take profit, taille max
- **Mode Simulation** : Testez sans risquer d'argent réel

### ✅ Phase 5 : Dashboard Web
- **Interface Moderne** : Visualisation des données en temps réel
- **Leaderboard** : Classement des meilleures whales
- **Historique** : Suivi des trades copiés

## 📊 Résultats

Le scanner a détecté **63 whales** sur 278 traders analysés :
- Top whale : **$54,885** de volume
- Données sauvegardées dans `whales.json`

## 🚀 Installation

### Prérequis
- Python 3.8+
- Un RPC Polygon (gratuit sur [Alchemy](https://www.alchemy.com/) ou [Infura](https://infura.io/))

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/minculusofia-wq/polymarket-bot.git
cd polymarket-bot
```

2. **Créer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre RPC URL
```

## 📖 Utilisation

### 1. Lancer le Bot (Scanner + Trader)
```bash
python scanner.py
```
Le bot va :
- Scanner le marché en continu
- Identifier les whales
- Exécuter des trades (paper trading par défaut)

### 2. Lancer le Dashboard
```bash
python api.py
```
Ouvrez votre navigateur sur `http://localhost:5000` pour voir :
- Le leaderboard des whales
- Les positions ouvertes
- L'historique des trades

## 📁 Structure du Projet

```
polymarket-bot/
├── scanner.py           # Bot principal (Scanner + Trader)
├── trader.py            # Module d'exécution des trades
├── whale_analyzer.py    # Module d'analyse et scoring
├── config.py            # Configuration du bot
├── api.py               # Serveur API pour le dashboard
├── dashboard/           # Interface Web
│   ├── index.html
│   ├── style.css
│   └── app.js
├── whales.json          # Base de données des whales
├── trade_history.json   # Historique des trades
└── README.md            # Documentation
```

## 🔧 Configuration

### Variables d'environnement (`.env`)

```env
# RPC Polygon (obligatoire)
POLYGON_RPC_URL=https://polygon-rpc.com

# Clé privée (pour le trading réel)
PRIVATE_KEY=votre_cle_privee_ici
```

### Configuration du Bot (`config.py`)

```python
PAPER_TRADING = True        # False pour trading réel
MAX_POSITION_SIZE_USD = 10  # Taille max par trade
STOP_LOSS_PERCENT = 0.15    # Stop loss à 15%
MIN_WHALE_SCORE = 60        # Score min pour copier
```

⚠️ **Sécurité** : Ne partagez jamais votre fichier `.env` ou votre clé privée !

## 📊 Format des Données

### `whales.json`
```json
{
  "0xWalletAddress": {
    "total_volume": 6527.4,
    "trade_count": 1,
    "markets": ["0x6903b766..."],
    "first_seen": 1764508266,
    "last_trade": 1764508266
  }
}
```

## 🛠️ Approche Technique

### Pivot Stratégique
L'approche initiale (endpoint `/holders`) a été abandonnée au profit d'une analyse des **trades récents** :

**Avantages :**
- ✅ Plus robuste (pas de dépendance à des champs manquants)
- ✅ Identifie les traders **actifs** (pas seulement les détenteurs passifs)
- ✅ Données riches (historique, marchés, timestamps)

### APIs Utilisées
- **Polymarket Data API** : `/trades` endpoint
- **Polygon RPC** : Connexion blockchain
- **Gamma API** : Recherche de marchés (tests)

## 🔮 Roadmap

- [x] Phase 1 : Infrastructure & Connexion
- [x] Phase 2 : Scanner de Whales
- [ ] Phase 3 : Copy-Trading automatique
- [ ] Phase 4 : Alertes Discord/Telegram
- [ ] Phase 5 : Dashboard web

## ⚠️ Avertissements

- **Risque financier** : Le trading comporte des risques. N'investissez que ce que vous pouvez vous permettre de perdre.
- **Sécurité** : Utilisez un wallet dédié avec peu de fonds pour les tests.
- **Maintenance** : Les APIs peuvent changer. Le bot nécessite une surveillance.

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

---

**Développé avec l'aide de l'IA** 🤖
