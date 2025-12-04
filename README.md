# Maison Manoé - E-commerce

Site e-commerce pour la décoration d'intérieur artisanale française.

## Installation

1. Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancer l'application :

```bash
python main.py
```

ou

```bash
uvicorn main:app --reload
```

4. Ouvrir dans le navigateur :

- Site web : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## Structure du projet

```
maison-manoe/
├── main.py              # Application FastAPI principale
├── templates/           # Templates HTML (Jinja2)
│   └── index.html      # Page d'accueil
├── static/             # Fichiers statiques (CSS, JS, images)
│   └── images/         # Images du site
├── requirements.txt    # Dépendances Python
├── .env.example       # Exemple de configuration
└── README.md          # Documentation
```

## Fonctionnalités prévues

- ✅ Page d'accueil
- 🔄 Page de recherche
- 🔄 Panier d'achat
- 🔄 Page à propos
- 🔄 Page de confidentialité
- 🔄 Page profil utilisateur
- 🔄 Page favoris
- 🔄 Module de paiement
- 🔄 Interface d'administration
- 🔄 Système de connexion

## Technologies

- **Backend** : FastAPI (Python)
- **Frontend** : HTML, Tailwind CSS
- **Templating** : Jinja2
