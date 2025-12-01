# 🔑 Guide : Obtenir les Clés API

Pour activer les fonctionnalités avancées (News & Reddit), suivez ces étapes simples (5 minutes max).

## 1. NewsAPI (Actualités)
*Gratuit pour le développement.*

1.  Allez sur **[https://newsapi.org/register](https://newsapi.org/register)**.
2.  Remplissez le formulaire (Nom, Email, Mot de passe).
3.  Choisissez "I am an individual".
4.  Une fois inscrit, votre **API Key** s'affiche directement.
    *   *Exemple : `a1b2c3d4e5...`*

---

## 2. Reddit API (Sentiment Social)
*Gratuit.*

1.  Connectez-vous à votre compte Reddit.
2.  Allez sur **[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)**.
3.  Cliquez sur le bouton **"are you a developer? create an app..."** (ou "create another app").
4.  Remplissez comme suit :
    *   **name** : `polymarket-bot`
    *   **Sélectionnez** : `script` (Très important !)
    *   **description** : (laisser vide)
    *   **about url** : (laisser vide)
    *   **redirect uri** : `http://localhost:8080`
5.  Cliquez sur **"create app"**.
6.  Vous avez besoin de 2 infos :
    *   **Client ID** : Le code juste sous le nom de l'app (ex: `XyZ_123abc`).
    *   **Client Secret** : Le code à côté de "secret" (ex: `A1B2-c3d4...`).

---

## 3. Où mettre ces clés ?

Une fois que vous les avez, copiez-les et collez-les ici dans le chat sous ce format :

```
NEWS_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
```

Je m'occuperai de les configurer pour vous ! 🚀
