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

### 🚧 Phase 3 : Copy-Trading (À venir)
- Surveillance en temps réel des whales
- Exécution automatique d'ordres
- Règles de sécurité (stop loss, taille max)

## 📊 Résultats

Le scanner a détecté **45 whales** sur 196 traders analysés :
- Top whale : **$6,527** de volume
- Données sauvegardées dans `whales.json`

## 🚀 Installation

### Prérequis
- Python 3.8+
- Un RPC Polygon (gratuit sur [Alchemy](https://www.alchemy.com/) ou [Infura](https://infura.io/))

### Étapes

1. **Cloner le repository**
```bash
git clone <votre-repo-url>
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

### Tester la connexion Polygon
```bash
python main.py
```

### Lancer le scanner de whales
```bash
python scanner.py
```

Le scanner va :
1. Récupérer les 1000 derniers trades
2. Analyser les traders par volume
3. Filtrer les whales (volume ≥ $100)
4. Sauvegarder les résultats dans `whales.json`

## 📁 Structure du Projet

```
polymarket-bot/
├── main.py              # Test de connexion Polygon
├── scanner.py           # Scanner de whales (trades-based)
├── requirements.txt     # Dépendances Python
├── .env.example         # Template de configuration
├── .gitignore          # Fichiers à ignorer
├── whales.json         # Base de données des whales (généré)
└── README.md           # Ce fichier
```

## 🔧 Configuration

### Variables d'environnement (`.env`)

```env
# RPC Polygon (obligatoire)
POLYGON_RPC_URL=https://polygon-rpc.com

# Clé privée (pour le trading - Phase 3)
PRIVATE_KEY=votre_cle_privee_ici

# API Polymarket (optionnel)
POLYMARKET_API_KEY=
POLYMARKET_API_SECRET=
POLYMARKET_PASSPHRASE=
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
