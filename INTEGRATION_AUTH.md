# Intégration Authentification Frontend - Maison Manoé

## 📋 Vue d'ensemble

Les pages d'authentification sont maintenant connectées à l'API JWT backend. Les utilisateurs peuvent s'inscrire, se connecter et accéder à leur profil de manière sécurisée.

## ✅ Modifications effectuées

### 1. Fichier JavaScript utilitaire (`/static/js/auth.js`)

Un module complet pour gérer l'authentification côté client :

**Fonctions principales :**

- `isAuthenticated()` - Vérifie si l'utilisateur est connecté
- `getCurrentUser()` - Récupère les infos de l'utilisateur
- `login(email, password, remember)` - Connexion avec l'API
- `register(userData)` - Inscription avec l'API
- `logout()` - Déconnexion
- `authenticatedFetch(endpoint, options)` - Requêtes API authentifiées
- `updateAuthUI()` - Met à jour l'interface selon l'état d'authentification
- `requireAuth()` - Protège une page (redirige si non connecté)

**Stockage :**

- `localStorage` : Si "Se souvenir de moi" est coché
- `sessionStorage` : Sinon (expire à la fermeture du navigateur)

**Clés de stockage :**

- `maison_manoe_token` : Token JWT
- `maison_manoe_token_type` : Type de token (bearer)
- `maison_manoe_user` : Données utilisateur (JSON)

### 2. Page de connexion (`/templates/auth/connexion.html`)

**Avant :**

```javascript
// Simulation avec setTimeout et Math.random()
```

**Après :**

```javascript
// Vraie connexion API
const response = await fetch("/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email, password }),
});
```

**Fonctionnalités :**

- ✅ Connexion réelle avec l'API `/api/auth/login`
- ✅ Récupération du profil utilisateur `/api/auth/me`
- ✅ Stockage du token JWT
- ✅ Option "Se souvenir de moi" (localStorage vs sessionStorage)
- ✅ Gestion des erreurs (401, 403, network)
- ✅ Redirection vers la page d'origine ou le profil
- ✅ Affichage spinner pendant le chargement

### 3. Page d'inscription (`/templates/auth/inscription.html`)

**Avant :**

```javascript
// Simulation avec setTimeout
```

**Après :**

```javascript
// Vraie inscription API
const response = await fetch("/api/auth/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email,
    password,
    first_name,
    last_name,
    phone,
  }),
});
```

**Fonctionnalités :**

- ✅ Inscription réelle avec l'API `/api/auth/register`
- ✅ Validation côté client (email, mot de passe, confirmation)
- ✅ Vérification des CGV acceptées
- ✅ Gestion des erreurs (email déjà utilisé, etc.)
- ✅ Message de succès avec redirection vers connexion
- ✅ Processus en 2 étapes (infos personnelles → sécurité)

### 4. Template de base (`/templates/client/base.html`)

**Ajouts :**

```html
<!-- Chargement du module auth -->
<script src="/static/js/auth.js"></script>

<!-- Initialisation UI -->
<script>
  window.MaisonManoeAuth.updateAuthUI();
  // Mise à jour icône utilisateur
  // Ajout tooltip avec nom utilisateur
</script>
```

**Fonctionnalités :**

- ✅ Chargement automatique du module auth
- ✅ Mise à jour de l'interface selon l'état de connexion
- ✅ Icône utilisateur dynamique (connexion vs profil)
- ✅ Tooltip avec le nom de l'utilisateur connecté

### 5. Layout auth (`/templates/auth/auth-layout.html`)

**Ajouts :**

```html
<!-- Chargement du module auth -->
<script src="/static/js/auth.js"></script>
```

## 🎯 Utilisation

### Tester l'inscription

1. Aller sur http://localhost:8000/inscription
2. Remplir le formulaire :
   - Civilité, prénom, nom
   - Email valide
   - Téléphone (optionnel)
   - Mot de passe (min 8 caractères)
   - Accepter les CGV
3. Cliquer sur "Créer mon compte"
4. Vérifier dans la console Network : `POST /api/auth/register`
5. Message de succès → Redirection vers connexion

### Tester la connexion

1. Aller sur http://localhost:8000/connexion
2. Entrer email et mot de passe
3. Cocher "Se souvenir de moi" (optionnel)
4. Cliquer sur "Se connecter"
5. Vérifier dans la console Network :
   - `POST /api/auth/login` → Token JWT
   - `GET /api/auth/me` → Profil utilisateur
6. Redirection vers /profile ou page d'origine

### Vérifier le stockage

**Ouvrir DevTools → Application/Storage :**

Si "Se souvenir de moi" coché :

```
localStorage:
  maison_manoe_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  maison_manoe_token_type: "bearer"
  maison_manoe_user: '{"id":"...","email":"...","first_name":"...",...}'
```

Sinon :

```
sessionStorage:
  (mêmes clés)
```

### Utiliser dans une page

```html
<!-- Afficher seulement si connecté -->
<div data-auth-required>
  <p>Bienvenue <span data-user-first-name></span>!</p>
</div>

<!-- Afficher seulement si non connecté -->
<div data-auth-guest>
  <a href="/connexion">Se connecter</a>
</div>

<script>
  // Protéger une page
  MaisonManoeAuth.requireAuth();

  // Récupérer l'utilisateur
  const user = MaisonManoeAuth.getCurrentUser();
  console.log(user.email);

  // Faire une requête authentifiée
  const response = await MaisonManoeAuth.authenticatedFetch('/api/products', {
    method: 'POST',
    body: { name: 'Nouveau produit' }
  });

  // Déconnexion
  MaisonManoeAuth.logout();
</script>
```

## 🔐 Sécurité

### Token JWT

- ✅ Stocké en localStorage ou sessionStorage (pas de cookies)
- ✅ Envoyé dans header `Authorization: Bearer <token>`
- ✅ Expiration : 30 minutes (configurable)
- ✅ Redirection auto si token expiré (401)

### Mots de passe

- ✅ Hashés avec bcrypt côté backend
- ✅ Minimum 8 caractères
- ✅ Indicateur de force en temps réel
- ✅ Confirmation obligatoire

### CORS

- ✅ Same-origin policy (frontend et backend sur même domaine)
- ✅ Pas de CORS nécessaire en production

## 🧪 Tests manuels

### Test 1 : Inscription

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@maisonmanoe.fr",
    "password": "Test123456!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Test 2 : Connexion

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@maisonmanoe.fr",
    "password": "Test123456!"
  }'
```

### Test 3 : Profil

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## 📝 TODO

### Court terme

- [ ] Page de profil utilisateur complète
- [ ] Modifier les informations personnelles
- [ ] Changement de mot de passe
- [ ] Historique des commandes

### Moyen terme

- [ ] Réinitialisation mot de passe par email
- [ ] Confirmation email d'inscription
- [ ] Authentification sociale (Google, Facebook)
- [ ] 2FA pour les comptes admin

### Long terme

- [ ] Refresh tokens (pour sessions longues)
- [ ] Rate limiting sur login
- [ ] Journalisation des connexions
- [ ] Gestion des sessions actives

## 🐛 Résolution de problèmes

### Le token n'est pas stocké

- Vérifier la console : erreurs JavaScript ?
- Vérifier Network : réponse 200 ?
- Vérifier que auth.js est bien chargé

### Erreur 401 "Could not validate credentials"

- Token expiré (30 min par défaut)
- Token invalide ou corrompu
- Secret key changée côté backend

### L'utilisateur n'est pas reconnu après rafraîchissement

- Vérifier localStorage/sessionStorage
- Nettoyer le cache du navigateur
- Vérifier que "Se souvenir de moi" était coché

### Erreur CORS

- Backend et frontend doivent être sur même origine
- Ou configurer CORS dans FastAPI :

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

## 🚀 Déploiement

En production, pensez à :

1. Utiliser HTTPS (obligatoire pour sécurité)
2. Changer la `SECRET_KEY` dans `.env`
3. Configurer les cookies HttpOnly + Secure
4. Activer le rate limiting
5. Monitorer les tentatives de connexion échouées
6. Utiliser des refresh tokens
7. Configurer CSP headers

## 📚 Ressources

- [AUTH.md](/AUTH.md) - Documentation complète de l'authentification
- [EXEMPLES_AUTH.py](/EXEMPLES_AUTH.py) - Exemples d'utilisation
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - Décodeur de tokens
