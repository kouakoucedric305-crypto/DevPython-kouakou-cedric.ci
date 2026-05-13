"""
=============================================================
  WSGI - Interface entre Django et le serveur web
=============================================================
WSGI (Web Server Gateway Interface) est le standard Python
pour la communication entre le serveur web et l'application.
Utilisé par Gunicorn, uWSGI en production.
"""

import os
from django.core.wsgi import get_wsgi_application

# Définit quel fichier settings utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entreprise_site.settings')

application = get_wsgi_application()
