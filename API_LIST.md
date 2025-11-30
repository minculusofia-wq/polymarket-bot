# Liste des APIs, RPC et WebSockets

Pour passer au niveau supérieur (Trading Haute Fréquence, Sniping), voici les services additionnels utiles :

## 1. WebSockets (Pour la vitesse ⚡️)

Les WebSockets permettent de recevoir les données en **temps réel** (push) au lieu de demander toutes les X secondes (poll).

### A. Polymarket CLOB WebSocket
*   **URL** : `wss://ws-subscriptions-clob.polymarket.com/ws/market`
*   **Utilité** :
    *   Recevoir les nouveaux ordres instantanément (avant qu'ils n'apparaissent sur le site).
    *   Voir les trades en temps réel (pour copier les whales plus vite).
    *   Suivre l'évolution des prix milliseconde par milliseconde.
*   **Statut** : *Non implémenté (Le bot utilise actuellement l'API REST `/trades`)*.

### B. Polygon WebSocket (Alchemy)
*   **URL** : `wss://polygon-mainnet.g.alchemy.com/v2/VOTRE_CLE`
*   **Utilité** :
    *   Détecter les transactions en attente (Mempool).
    *   Savoir quand votre trade est confirmé sur la blockchain instantanément.

## 2. API Keys (Pour le Trading Réel 💰)

Pour placer des ordres réels sur Polymarket (pas seulement Paper Trading), vous devez générer des clés API sur [polymarket.com/profile/api-keys](https://polymarket.com/profile/api-keys).

*   **API Key**
*   **API Secret**
*   **Passphrase**

Ces clés permettent de signer des ordres sans avoir à approuver chaque transaction manuellement dans MetaMask.

## 3. Services Optionnels

*   **Telegram Bot API** : Pour recevoir des alertes sur votre téléphone quand une whale achète.
*   **Discord Webhook** : Pour envoyer les alertes dans un canal Discord.

---

## Configuration Actuelle du Bot

| Service | Type | Usage Actuel | Statut |
|---------|------|--------------|--------|
| **Polygon RPC** | HTTP | Lire les balances | ✅ Configuré (Alchemy) |
| **Data API** | HTTP | Scanner les trades | ✅ Utilisé |
| **Gamma API** | HTTP | Infos marchés | ✅ Utilisé |
| **CLOB WebSocket** | WSS | Flux temps réel | ❌ Non utilisé (Potentiel d'amélioration) |
