"""URLs de l'application core."""
from django.urls import path
from . import views

urlpatterns = [
    path('',           views.accueil,   name='accueil'),
    path('a-propos/',  views.a_propos,  name='a_propos'),
    path('services/',  views.services,  name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('equipe/',    views.equipe,    name='equipe'),
    path('contact/',   views.contact,   name='contact'),
]
