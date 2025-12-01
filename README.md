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

### ✅ Phase 6 : Performance (WebSocket)
- **Détection Temps Réel** : Latence proche de zéro
- **Connexion Sécurisée** : Support SSL/TLS
- **Sniping Ready** : Réaction instantanée aux mouvements de marché

### ✅ Phase 7 : Opportunités & Data
- **Scanner de Marché** : Détection des tendances et mouvements de prix
- **News Aggregator** : NewsAPI + CoinStats
- **Social Sentiment** : Reddit (r/CryptoCurrency)
- **Événements** : CoinGecko Events
- **Vidéos** : YouTube Search (SerpAPI)

### ✅ Phase 8 : Configuration Avancée
- **Whitelist Manuelle** : Ajoutez des wallets spécifiques à copier
- **Configuration du Wallet** : Entrez votre clé privée depuis le Dashboard
- **Toggle Paper/Real** : Basculez entre modes directement dans l'interface
- **Settings Éditables** : Modifiez tous les paramètres en temps réel

### ✅ Phase 9 : Signaux Convergents
- **Détection Intelligente** : Croise les données whales + opportunités
- **Seuils Configurables** : Min Whales (1-5) + Min Sources (1-5)
- **Score de Confiance** : Affiche uniquement les signaux à haute probabilité
- **Détails Expandables** : Voir les whales et sources pour chaque signal

## 📊 Résultats

Le scanner a détecté **63 whales** sur 278 traders analysés :
- Top whale : **$54,885** de volume
- Données sauvegardées dans `whales.json`

## 🚀 Installation

### Prérequis
- Python 3.8+
- Un RPC Polygon (gratuit sur [Alchemy](https://www.alchemy.com/) ou [Infura](https://infura.io/))
- (Optionnel) Clés API pour les données externes

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/minculusofia-wq/polymarket-bot.git
cd polymarket-bot
```

2. **Lancer le script d'installation automatique**
```bash
./start_bot.command
```
Ce script va créer l'environnement virtuel, installer les dépendances et lancer le bot.

### Configuration Avancée (`config.py`)

Pour activer toutes les fonctionnalités de données externes, ajoutez vos clés dans `config.py` ou `.env` :

```python
# External Data Sources
NEWS_API_KEY = "votre_cle"
LUNARCRUSH_API_KEY = "votre_cle"
SERPAPI_KEY = "votre_cle"
HELIUS_API_KEY = "votre_cle"
```

Voir `API_KEYS_GUIDE.md` pour obtenir ces clés gratuitement.

## 📖 Utilisation

### 🚀 Lancement Facile (Recommandé)
Double-cliquez simplement sur le fichier `start_bot.command` !

Cela va automatiquement :
1. Lancer le Dashboard API
2. Ouvrir le Dashboard dans votre navigateur (`http://localhost:5000`)
3. Lancer le Scanner WebSocket en arrière-plan

### Dashboard
Le dashboard offre plusieurs onglets :
- **Stats & Whales** : Suivi des gros traders avec adresses complètes (bouton copie)
- **Settings** : Configuration en temps réel (Stop Loss, Capital, Mode Trading...)
- **Whitelist** : Ajoutez manuellement des wallets à copier
- **Wallet Config** : Configurez votre clé privée pour le trading réel
- **Opportunités** : News, Reddit, Événements, Vidéos
- **🎯 Signaux Convergents** : Détection automatique des opportunités à haute confiance

## 📁 Structure du Projet

```
polymarket-bot/
├── scanner_ws.py        # Scanner Temps Réel (WebSocket)
├── opportunities.py     # Scanner d'opportunités (News, Social)
├── convergent_signals.py # Détection de signaux convergents
├── external_scanner.py  # Gestion des APIs externes
├── trader.py            # Module d'exécution des trades
├── whale_analyzer.py    # Module d'analyse et scoring
├── config.py            # Configuration du bot
├── api.py               # Serveur API pour le dashboard
├── dashboard/           # Interface Web
│   ├── index.html
│   ├── style.css
│   └── app.js
├── whales.json          # Base de données des whales
├── whitelist.json       # Wallets à copier manuellement
├── convergent_signals.json # Signaux détectés
└── README.md            # Documentation
```

## 🔮 Roadmap

- [x] Phase 1 : Infrastructure & Connexion
- [x] Phase 2 : Scanner de Whales
- [x] Phase 3 : Copy-Trading automatique
- [x] Phase 4 : Dashboard web
- [x] Phase 5 : WebSocket & Performance
- [x] Phase 6 : Agrégateur de Données (News, Social)
- [ ] Phase 7 : Alertes Discord/Telegram
- [ ] Phase 8 : Trading Réel (Mainnet)

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
