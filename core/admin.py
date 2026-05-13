"""
Administration Django — Application core.
Le CMS est entièrement géré ici.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, PageBlock,
    Service, Projet, MembreEquipe, Temoignage, MessageContact
)

# ── CMS ──────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Paramètres globaux du site (singleton)."""
    fieldsets = (
        ('🏢 Identité', {'fields': ('nom_entreprise', 'slogan', 'meta_description')}),
        ('📍 Coordonnées', {'fields': ('adresse', 'telephone', 'email_contact', 'email_support', 'horaires')}),
        ('🌐 Réseaux sociaux', {'fields': ('url_linkedin', 'url_twitter', 'url_facebook', 'url_instagram')}),
    )

    def has_add_permission(self, request):
        # Empêcher d'en créer un deuxième
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Ne pas supprimer le singleton


@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    """Blocs de contenu éditables par page."""
    list_display  = ['label', 'page', 'cle', 'type', 'apercu']
    list_filter   = ['page', 'type']
    search_fields = ['label', 'cle', 'valeur']
    list_editable = []
    ordering      = ['page', 'cle']

    def apercu(self, obj):
        """Affiche les 60 premiers caractères du contenu."""
        return obj.valeur[:60] + '…' if len(obj.valeur) > 60 else obj.valeur
    apercu.short_description = "Aperçu"

    actions = ['initialiser_blocs_accueil']

    def initialiser_blocs_accueil(self, request, queryset):
        """Action : crée les blocs de démo pour la page d'accueil."""
        defaults = [
            ('accueil','hero_titre','text','Titre Hero',"Transformez vos idées en solutions innovantes"),
            ('accueil','hero_sous','text','Sous-titre Hero',"Nous accompagnons les entreprises dans leur transformation digitale."),
            ('a_propos','histoire_titre','text','Titre Histoire',"Notre Histoire"),
            ('a_propos','histoire_texte','textarea','Texte Histoire',"Fondée en 2011, MonEntreprise est née de la vision de trois entrepreneurs passionnés."),
            ('contact','hero_titre','text','Titre Contact',"Contactez-nous"),
            ('contact','hero_sous','text','Sous-titre Contact',"Parlons de votre projet."),
        ]
        created = 0
        for page, cle, type_, label, valeur in defaults:
            obj, was_created = PageBlock.objects.get_or_create(
                page=page, cle=cle,
                defaults={'type':type_, 'label':label, 'valeur':valeur}
            )
            if was_created:
                created += 1
        self.message_user(request, f"{created} bloc(s) initialisé(s).")
    initialiser_blocs_accueil.short_description = "🔧 Initialiser les blocs de démo"


# ── SERVICES ────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['titre', 'icone_preview', 'ordre', 'actif']
    list_filter   = ['actif']
    list_editable = ['ordre', 'actif']
    search_fields = ['titre']

    def icone_preview(self, obj):
        return format_html('<i class="fas {}"></i> <code>{}</code>', obj.icone, obj.icone)
    icone_preview.short_description = "Icône"


# ── PROJETS ─────────────────────────────────────────────

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display  = ['titre', 'client', 'categorie', 'date_realisation', 'en_vedette']
    list_filter   = ['en_vedette', 'categorie']
    list_editable = ['en_vedette']
    search_fields = ['titre', 'client', 'technologies']
    fieldsets = (
        ('Informations', {'fields': ('titre', 'client', 'categorie', 'description', 'date_realisation')}),
        ('Médias & Liens', {'fields': ('image', 'lien', 'technologies')}),
        ('Options', {'fields': ('en_vedette',)}),
    )


# ── ÉQUIPE ──────────────────────────────────────────────

@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display  = ['nom_complet', 'poste', 'ordre']
    list_editable = ['ordre']
    search_fields = ['prenom', 'nom', 'poste']


# ── TÉMOIGNAGES ─────────────────────────────────────────

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display  = ['nom_client', 'entreprise_client', 'note', 'approuve', 'date_ajout']
    list_filter   = ['approuve', 'note']
    list_editable = ['approuve']
    actions       = ['approuver']

    def approuver(self, request, queryset):
        n = queryset.update(approuve=True)
        self.message_user(request, f"{n} témoignage(s) approuvé(s).")
    approuver.short_description = "✅ Approuver la sélection"


# ── MESSAGES DE CONTACT ─────────────────────────────────

@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'email', 'service_souhaite', 'date_envoi', 'lu', 'repondu']
    list_filter   = ['lu', 'repondu', 'service_souhaite']
    list_editable = ['lu', 'repondu']
    readonly_fields = ['nom','email','entreprise','telephone','service_souhaite','message','date_envoi']
    search_fields = ['nom', 'email', 'message']
    ordering      = ['lu', '-date_envoi']


# ── PERSONNALISATION ADMIN ──────────────────────────────
admin.site.site_header  = "🏢 MonEntreprise — Administration"
admin.site.site_title   = "Admin MonEntreprise"
admin.site.index_title  = "Tableau de bord CMS"
