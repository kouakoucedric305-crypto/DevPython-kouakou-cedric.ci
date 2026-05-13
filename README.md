# 🏢 MonEntreprise — Site Corporate Django

Site d'entreprise complet avec CMS intégré, développé avec Django 4.x.

## 📦 Installation

```bash
# 1. Installer les dépendances
pip install django pillow

# 2. Appliquer les migrations
python manage.py migrate

# 3. Créer un administrateur
python manage.py createsuperuser

# 4. Lancer le serveur de développement
python manage.py runserver
```

Le site est accessible à : **http://127.0.0.1:8000/**

## 🗺️ Pages disponibles

| URL | Page |
|-----|------|
| `/` | Accueil |
| `/a-propos/` | À propos |
| `/services/` | Services |
| `/portfolio/` | Portfolio |
| `/equipe/` | Équipe |
| `/contact/` | Contact |
| `/admin/` | Administration CMS |

## ⚙️ CMS — Gestion du contenu

Connectez-vous à `/admin/` avec vos identifiants admin.

### Ce que vous pouvez gérer :

| Section | Description |
|---------|-------------|
| **Paramètres du site** | Nom, adresse, email, réseaux sociaux |
| **Blocs de contenu** | Textes éditables de chaque page (titres, paragraphes) |
| **Services** | Ajouter/modifier/supprimer des services |
| **Projets** | Gérer le portfolio |
| **Équipe** | Membres de l'équipe |
| **Témoignages** | Avis clients (approbation manuelle) |
| **Messages de contact** | Consulter les messages reçus |

### 🔧 Initialiser les blocs de contenu

1. Aller dans **Blocs de contenu**
2. Sélectionner tous → Action : **"Initialiser les blocs de démo"**
3. Les champs éditables des pages sont créés automatiquement

## 🛠️ Structure du projet

```
entreprise_site/
├── manage.py
├── entreprise_site/        ← Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                   ← Application principale
    ├── models.py            ← Modèles (+ CMS)
    ├── views.py             ← Logique des pages
    ├── forms.py             ← Formulaire de contact
    ├── admin.py             ← Interface admin CMS
    ├── urls.py              ← Routage URLs
    ├── templates/core/      ← Templates HTML
    │   ├── base.html        ← Header + Footer communs
    │   ├── accueil.html
    │   ├── services.html
    │   ├── portfolio.html
    │   ├── equipe.html
    │   ├── a_propos.html
    │   └── contact.html
    ├── static/core/
    │   ├── css/style.css    ← Design fidèle au maquette
    │   └── js/main.js       ← Interactivité
    └── migrations/

```

## 🔑 Compte admin (développement)

- **URL** : http://127.0.0.1:8000/admin/
- **Login** : `admin`
- **Mot de passe** : `admin123`

⚠️ Changer le mot de passe avant mise en production !

## 🚀 Mise en production

1. Mettre `DEBUG = False` dans `settings.py`
2. Générer une vraie `SECRET_KEY`
3. Configurer `ALLOWED_HOSTS`
4. Utiliser PostgreSQL à la place de SQLite
5. Configurer un serveur email SMTP
6. Exécuter `python manage.py collectstatic`
7. Déployer avec Gunicorn + Nginx
