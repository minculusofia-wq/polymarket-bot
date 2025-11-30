# Instructions pour créer le repository GitHub

## Option 1 : Via l'interface GitHub (Recommandé)

1. **Aller sur GitHub** : https://github.com/new

2. **Remplir le formulaire** :
   - **Repository name** : `polymarket-bot`
   - **Description** : `Bot de trading automatisé pour Polymarket - Scanner de whales et copy-trading`
   - **Visibilité** : Public (ou Private si vous préférez)
   - **NE PAS cocher** :
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

3. **Cliquer sur "Create repository"**

4. **Copier l'URL du repository** qui apparaît (format : `https://github.com/VOTRE_USERNAME/polymarket-bot.git`)

5. **Revenir dans le terminal** et exécuter ces commandes :

```bash
cd /Users/anthony/Desktop/gradient-optimizer/polymarket-bot

# Ajouter le remote GitHub (remplacez VOTRE_USERNAME par votre nom d'utilisateur)
git remote add origin https://github.com/VOTRE_USERNAME/polymarket-bot.git

# Pousser le code
git branch -M main
git push -u origin main
```

## Option 2 : Via GitHub CLI (si installé)

```bash
cd /Users/anthony/Desktop/gradient-optimizer/polymarket-bot

# Créer le repository et pousser le code
gh repo create polymarket-bot --public --source=. --remote=origin --push
```

## Vérification

Une fois le push terminé, votre repository sera visible sur :
`https://github.com/VOTRE_USERNAME/polymarket-bot`

## Fichiers qui seront poussés

- ✅ `README.md` - Documentation complète
- ✅ `scanner.py` - Scanner de whales
- ✅ `main.py` - Test de connexion
- ✅ `requirements.txt` - Dépendances
- ✅ `.env.example` - Template de configuration
- ✅ `.gitignore` - Fichiers à ignorer
- ✅ `whales.json` - Données des whales détectées
- ✅ Scripts de test et recherche

**Note** : Le fichier `.env` (avec vos clés) ne sera PAS poussé grâce au `.gitignore` 🔒
