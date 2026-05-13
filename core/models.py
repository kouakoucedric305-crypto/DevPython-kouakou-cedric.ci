"""
Modèles métier + CMS pour l'application core.
CMS = SiteSettings (paramètres globaux) + PageBlock (blocs éditables par page).
"""
from django.db import models


# ── CMS : PARAMÈTRES GLOBAUX ──────────────────────────────
class SiteSettings(models.Model):
    """Singleton : paramètres du site éditables via l'admin."""
    nom_entreprise   = models.CharField(max_length=100, default="MonEntreprise")
    slogan           = models.CharField(max_length=200, default="Solutions innovantes pour votre entreprise")
    adresse          = models.TextField(default="123 Rue de l'Innovation, 75001 Paris")
    telephone        = models.CharField(max_length=30, default="+33 1 23 45 67 89")
    email_contact    = models.EmailField(default="contact@monentreprise.fr")
    email_support    = models.EmailField(blank=True)
    horaires         = models.TextField(default="Lun-Ven : 9h00 - 18h00\nSamedi : 10h00 - 13h00")
    url_linkedin     = models.URLField(blank=True)
    url_twitter      = models.URLField(blank=True)
    url_facebook     = models.URLField(blank=True)
    url_instagram    = models.URLField(blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return f"Paramètres — {self.nom_entreprise}"

    def save(self, *args, **kwargs):
        self.pk = 1  # Forcer singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ── CMS : BLOCS DE CONTENU ────────────────────────────────
class PageBlock(models.Model):
    """
    Blocs de contenu éditables par page depuis l'admin.
    Identifiés par (page, cle). Valeur récupérée dans les vues
    et passée au template. Exemple : page='accueil', cle='hero_titre'.
    """
    PAGE_CHOICES = [
        ('accueil',  'Accueil'),
        ('a_propos', 'À propos'),
        ('services', 'Services'),
        ('portfolio','Portfolio'),
        ('equipe',   'Équipe'),
        ('contact',  'Contact'),
        ('global',   'Global'),
    ]
    TYPE_CHOICES = [
        ('text',     'Texte court'),
        ('textarea', 'Texte long'),
        ('html',     'HTML riche'),
    ]
    page   = models.CharField(max_length=20, choices=PAGE_CHOICES)
    cle    = models.SlugField(max_length=50, help_text="Ex: hero_titre")
    type   = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    label  = models.CharField(max_length=100, help_text="Description lisible pour l'admin")
    valeur = models.TextField(blank=True)

    class Meta:
        unique_together = ('page', 'cle')
        ordering = ['page', 'cle']
        verbose_name = "Bloc de contenu"
        verbose_name_plural = "Blocs de contenu"

    def __str__(self):
        return f"[{self.page}] {self.label}"


# ── SERVICE ───────────────────────────────────────────────
class Service(models.Model):
    titre              = models.CharField(max_length=100, verbose_name="Titre")
    description_courte = models.CharField(max_length=200, verbose_name="Description courte")
    description_longue = models.TextField(verbose_name="Description complète")
    fonctionnalites    = models.TextField(blank=True, help_text="Une fonctionnalité par ligne")
    icone  = models.CharField(max_length=50, default="fa-star", help_text="Classe FontAwesome (ex: fa-code)")
    ordre  = models.PositiveIntegerField(default=0)
    actif  = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.titre


# ── PROJET / PORTFOLIO ────────────────────────────────────
class Projet(models.Model):
    titre            = models.CharField(max_length=150)
    client           = models.CharField(max_length=100)
    categorie        = models.CharField(max_length=100, blank=True, help_text="Ex: Développement Web")
    description      = models.TextField()
    technologies     = models.CharField(max_length=200, help_text="Séparées par virgule: React, Python")
    image            = models.ImageField(upload_to='projets/', blank=True, null=True)
    lien             = models.URLField(blank=True)
    date_realisation = models.DateField()
    en_vedette       = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_realisation']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return f"{self.titre} ({self.client})"


# ── MEMBRE DE L'ÉQUIPE ────────────────────────────────────
class MembreEquipe(models.Model):
    prenom   = models.CharField(max_length=50)
    nom      = models.CharField(max_length=50)
    poste    = models.CharField(max_length=100)
    bio      = models.TextField()
    photo    = models.ImageField(upload_to='equipe/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    twitter  = models.URLField(blank=True)
    github   = models.URLField(blank=True)
    ordre    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.poste}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


# ── TÉMOIGNAGE ────────────────────────────────────────────
class Temoignage(models.Model):
    nom_client        = models.CharField(max_length=100)
    poste_client      = models.CharField(max_length=100)
    entreprise_client = models.CharField(max_length=100)
    message           = models.TextField()
    note              = models.PositiveIntegerField(default=5, choices=[(i, f"{i}★") for i in range(1, 6)])
    photo    = models.ImageField(upload_to='temoignages/', blank=True, null=True)
    approuve = models.BooleanField(default=False)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.nom_client} ({self.entreprise_client}) — {self.note}★"


# ── MESSAGE DE CONTACT ────────────────────────────────────
class MessageContact(models.Model):
    SERVICE_CHOICES = [
        ('web',      'Développement Web'),
        ('mobile',   'Application Mobile'),
        ('design',   'Design UI/UX'),
        ('marketing','Marketing Digital'),
        ('conseil',  'Conseil & Stratégie'),
        ('autre',    'Autre'),
    ]
    nom              = models.CharField(max_length=100)
    email            = models.EmailField()
    entreprise       = models.CharField(max_length=100, blank=True)
    telephone        = models.CharField(max_length=20, blank=True)
    service_souhaite = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
    message          = models.TextField()
    date_envoi       = models.DateTimeField(auto_now_add=True)
    lu               = models.BooleanField(default=False)
    repondu          = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"[{self.date_envoi.strftime('%d/%m/%Y')}] {self.nom} — {self.email}"
