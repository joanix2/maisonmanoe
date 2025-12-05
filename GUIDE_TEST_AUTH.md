# Guide de test - Authentification utilisateur

## 🎯 Fonctionnalités implémentées

### 1. Service et routes API ✅

- **UserService** : CRUD complet + authentification
- **Routes API** :
  - `POST /api/auth/register` - Inscription
  - `POST /api/auth/login` - Connexion
  - `GET /api/auth/me` - Profil utilisateur
  - `POST /api/auth/token` - Token OAuth2 (Swagger)

### 2. Page Profile ✅

- Affichage des informations personnelles
- Avatar avec initiales
- Badge administrateur si applicable
- Section informations, adresses, commandes, favoris, sécurité
- Bouton de déconnexion

### 3. Menu utilisateur dans le header ✅

- Dropdown avec menu contextuel
- Liens vers profil et favoris
- Bouton de déconnexion
- Adaptatif selon l'état de connexion

## 🧪 Comment tester

### Étape 1 : Inscription

1. Aller sur http://localhost:8000/inscription
2. Remplir le formulaire :
   - Civilité : M. / Mme / Autre
   - Prénom : Test
   - Nom : User
   - Email : test@example.com
   - Téléphone : +33 6 12 34 56 78 (optionnel)
   - Mot de passe : TestPassword123!
   - Confirmation : TestPassword123!
3. Accepter les CGV
4. Cliquer sur "Créer mon compte"
5. ✅ Vérifier le message de succès
6. ✅ Redirection automatique vers /connexion

### Étape 2 : Connexion

1. Sur la page de connexion
2. Entrer :
   - Email : test@example.com
   - Mot de passe : TestPassword123!
3. Cocher "Se souvenir de moi" (optionnel)
4. Cliquer sur "Se connecter"
5. ✅ Vérifier la redirection vers /profile

### Étape 3 : Page Profile

Sur la page profile, vérifier :

- ✅ Avatar avec initiales "TU"
- ✅ Nom complet affiché : "Test User"
- ✅ Email : test@example.com
- ✅ Téléphone : +33 6 12 34 56 78
- ✅ Date de création du compte
- ✅ Statut : Actif (vert)
- ✅ Badge admin si c'est un administrateur

### Étape 4 : Menu utilisateur (Header)

1. Cliquer sur l'icône utilisateur en haut à droite
2. ✅ Vérifier que le dropdown s'ouvre
3. ✅ Voir les options :
   - Mon profil
   - Mes favoris
   - --- (séparateur)
   - Se déconnecter (rouge)
4. Cliquer en dehors → Le menu se ferme
5. Appuyer sur Échap → Le menu se ferme

### Étape 5 : Déconnexion depuis le header

1. Cliquer sur l'icône utilisateur
2. Cliquer sur "Se déconnecter"
3. ✅ Confirmation demandée
4. Cliquer sur OK
5. ✅ Redirection vers la page d'accueil
6. ✅ Token supprimé (vérifier dans DevTools → Application → Storage)
7. ✅ Le menu utilisateur affiche maintenant "Se connecter" et "S'inscrire"

### Étape 6 : Déconnexion depuis le profile

1. Se reconnecter
2. Aller sur /profile
3. Dans le menu latéral gauche, cliquer sur "Se déconnecter"
4. ✅ Confirmation demandée
5. Cliquer sur OK
6. ✅ Redirection vers la page d'accueil

### Étape 7 : Protection de la page profile

1. Se déconnecter
2. Essayer d'accéder à http://localhost:8000/profile
3. ✅ Redirection automatique vers /connexion?return=/profile
4. Se connecter
5. ✅ Redirection automatique vers /profile

## 🔍 Vérifications techniques

### Vérifier le token dans le navigateur

1. Ouvrir DevTools (F12)
2. Aller dans **Application** → **Local Storage** (ou Session Storage)
3. Chercher :
   - `maison_manoe_token` : Le JWT
   - `maison_manoe_token_type` : "bearer"
   - `maison_manoe_user` : Objet JSON avec les données utilisateur

### Vérifier les appels API

1. Ouvrir DevTools (F12)
2. Aller dans l'onglet **Network**
3. Lors de la connexion, vérifier :
   - `POST /api/auth/login` → 200 OK, retourne le token
   - `GET /api/auth/me` → 200 OK, retourne l'utilisateur
4. Sur la page profile :
   - Le header `Authorization: Bearer <token>` est présent

### Vérifier dans Neo4j

1. Ouvrir Neo4j Browser : http://localhost:7474
2. Exécuter :

```cypher
MATCH (u:User)
RETURN u.email, u.first_name, u.last_name, u.is_active, u.is_admin, u.created_at
```

3. ✅ Voir votre utilisateur créé

### Vérifier les index

```cypher
SHOW INDEXES
```

Doit afficher :

- `user_id_index` sur User.id
- `user_email_index` sur User.email
- `product_vector_index` sur Product.embedding

## 🎨 Aperçu des fonctionnalités

### Page Profile - Section Informations

```
┌─────────────────────────────────────────┐
│ Informations personnelles       Modifier│
├─────────────────────────────────────────┤
│ Prénom              Nom                 │
│ Test                User                │
│                                         │
│ Email               Téléphone           │
│ test@example.com    +33 6 12 34 56 78  │
│                                         │
│ Compte créé le                          │
│ 5 décembre 2025                         │
│                                         │
│ 👑 Compte Administrateur (si admin)    │
└─────────────────────────────────────────┘
```

### Menu utilisateur (Header)

```
┌────────────────────┐
│ 👤 Mon profil      │
│ ❤️  Mes favoris     │
├────────────────────┤
│ 🚪 Se déconnecter  │ (rouge)
└────────────────────┘
```

## 🐛 Résolution de problèmes

### "Impossible de charger vos informations"

- Le token est peut-être expiré (30 min)
- Se reconnecter

### La page profile ne charge pas les données

- Ouvrir la console (F12)
- Vérifier les erreurs JavaScript
- Vérifier que `auth.js` est bien chargé

### Le dropdown ne s'ouvre pas

- Vérifier la console pour les erreurs
- Vérifier que le JavaScript de base.html est bien exécuté

### Le bouton de déconnexion ne fonctionne pas

- Vérifier que `MaisonManoeAuth.logout()` est appelé
- Vérifier que le localStorage est bien nettoyé après déconnexion

## 🚀 Prochaines étapes

- [ ] Protéger les routes admin avec `Depends(get_current_user_email)`
- [ ] Ajouter la modification du profil
- [ ] Implémenter le changement de mot de passe
- [ ] Ajouter la réinitialisation de mot de passe par email
- [ ] Implémenter les refresh tokens pour sessions longues
- [ ] Ajouter la gestion des adresses
- [ ] Lier les commandes à l'utilisateur

## 📊 Statistiques

- ✅ 3 routes API auth
- ✅ 1 service UserService complet
- ✅ 8 modèles Pydantic pour l'auth
- ✅ 2 index Neo4j créés automatiquement
- ✅ 1 page profile avec 5 sections
- ✅ 1 menu dropdown utilisateur
- ✅ 2 boutons de déconnexion (header + profile)
- ✅ Protection automatique de la page profile
- ✅ Token JWT avec expiration 30 min
- ✅ Mots de passe hashés avec bcrypt
