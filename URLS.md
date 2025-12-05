# Plan du site - Maison Manoé

## 🏠 Pages Client (Public)

### Pages principales

- **`/`** - Page d'accueil
- **`/recherche`** - Recherche de produits (paramètre `?q=terme`)
- **`/panier`** - Panier d'achat
- **`/favoris`** - Liste des favoris
- **`/profile`** - Profil utilisateur (protégé)

### Paiement

- **`/paiement`** - Page de paiement
- **`/validation-paiement`** - Confirmation de paiement

### Informations

- **`/contact`** - Formulaire de contact
- **`/a-propos`** - À propos de Maison Manoé
- **`/faq`** - Questions fréquentes

### Légal

- **`/cgv`** - Conditions générales de vente
- **`/confidentialite`** - Politique de confidentialité
- **`/retours`** - Retours et échanges
- **`/livraison`** - Informations sur la livraison

---

## 🔐 Pages Authentification

### Connexion / Inscription

- **`/inscription`** - Formulaire d'inscription
- **`/connexion`** - Formulaire de connexion

### Mot de passe

- **`/reset-password`** - Demande de réinitialisation de mot de passe
- **`/new-password`** - Définir un nouveau mot de passe

---

## 👑 Pages Admin (Protégées)

### Dashboard

- **`/admin`** - Tableau de bord administrateur

### Gestion

- **`/admin/promos`** - Gestion des promotions
- **`/admin/produits`** - Gestion des produits
- **`/admin/texte`** - Gestion des textes du site
- **`/admin/notifications`** - Page des notifications

---

## 🔌 API REST

### Authentification (`/api/auth`)

- **`POST /api/auth/register`** - Inscription d'un nouvel utilisateur
- **`POST /api/auth/login`** - Connexion (retourne JWT)
- **`POST /api/auth/token`** - Connexion OAuth2 (pour Swagger UI)
- **`GET /api/auth/me`** - Informations de l'utilisateur connecté (protégé)

### Produits (`/api/products`)

- **`GET /api/products`** - Liste des produits
  - Paramètres : `?category=`, `?status=`, `?limit=`, `?skip=`
- **`GET /api/products/{product_id}`** - Détails d'un produit
- **`POST /api/products`** - Créer un produit (admin)
- **`PUT /api/products/{product_id}`** - Modifier un produit (admin)
- **`DELETE /api/products/{product_id}`** - Supprimer un produit (admin)
- **`POST /api/products/search`** - Recherche sémantique de produits

---

## 📊 Statistiques

### Pages publiques : 14

- Accueil
- Recherche
- Panier
- Favoris
- Profile
- Paiement
- Validation paiement
- Contact
- À propos
- FAQ
- CGV
- Confidentialité
- Retours
- Livraison

### Pages authentification : 4

- Inscription
- Connexion
- Reset password
- New password

### Pages admin : 4

- Dashboard
- Gestion promos
- Gestion produits
- Gestion textes

### API endpoints : 10

- 4 endpoints auth
- 6 endpoints produits

**Total : 32 URLs**

---

## 🔗 Liens de navigation

### Header (menu principal)

- Accueil (/)
- Produits (/recherche)
- Nouveautés (/recherche?filter=nouveautes)
- Promotions (/recherche?filter=promotions)
- Recherche (/recherche)
- Favoris (/favoris)
- Panier (/panier)
- Profil (/profile ou /connexion)

### Footer

**Navigation**

- Accueil (/)
- Produits (/recherche)
- À propos (/a-propos)

**Support**

- FAQ (/faq)
- Contact (/contact)
- Livraison (/livraison)
- Retours (/retours)

**Légal**

- Confidentialité (/confidentialite)
- CGV (/cgv)

---

## 🎯 Pages avec filtres

### Page recherche

- `/recherche` - Tous les produits
- `/recherche?filter=nouveautes` - Nouveautés
- `/recherche?filter=promotions` - Promotions
- `/recherche?q=terme` - Recherche par mot-clé
- `/recherche?category=categorie` - Filtrer par catégorie

---

## 🔒 Protection des routes

### Pages protégées (nécessitent authentification)

- `/profile` - Profil utilisateur
- `/admin` - Dashboard admin
- `/admin/promos` - Gestion promos
- `/admin/produits` - Gestion produits
- `/admin/texte` - Gestion textes

### API protégée (nécessite token JWT)

- `GET /api/auth/me` - Profil utilisateur
- `POST /api/products` - Créer produit (admin)
- `PUT /api/products/{id}` - Modifier produit (admin)
- `DELETE /api/products/{id}` - Supprimer produit (admin)

---

## 📱 Routes statiques

### CSS

- `/static/css/*` - Fichiers CSS personnalisés

### JavaScript

- `/static/js/auth.js` - Module d'authentification client

### Images

- `/static/images/*` - Images et logos du site

---

## 🌐 Documentation API

### Swagger UI

- **`/docs`** - Interface Swagger (documentation interactive)

### ReDoc

- **`/redoc`** - Documentation ReDoc (alternative)

### OpenAPI Schema

- **`/openapi.json`** - Schéma OpenAPI JSON
