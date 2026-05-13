"""
=============================================================
  FICHIER DE ROUTAGE PRINCIPAL DES URLs
=============================================================
Ce fichier définit toutes les routes (URLs) du projet.
Django lit ce fichier pour savoir quelle vue appeler
selon l'URL demandée par l'utilisateur.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ─── Administration Django ────────────────────────────
    # Accessible à l'adresse : /admin/
    path('admin/', admin.site.urls),

    # ─── URLs de l'application principale ────────────────
    # Toutes les URLs de 'core' sont incluses à la racine
    # Ex: '/' -> core.urls -> vue accueil
    path('', include('core.urls')),
]

# ─── FICHIERS MÉDIAS EN DÉVELOPPEMENT ────────────────────
# En production, c'est le serveur web (Nginx/Apache) qui gère les médias
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
