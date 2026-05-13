"""
Vues Django — Application core.
Chaque vue passe les blocs CMS au template via get_blocs(page).
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import Service, Projet, MembreEquipe, Temoignage, PageBlock, SiteSettings
from .forms import FormulaireContact


def get_blocs(page):
    qs = PageBlock.objects.filter(page__in=[page, 'global'])
    return {b.cle: b.valeur for b in qs}


def accueil(request):
    return render(request, 'core/accueil.html', {
        'titre_page': 'Accueil',
        'blocs': get_blocs('accueil'),
        'settings': SiteSettings.get(),
    })


def a_propos(request):
    return render(request, 'core/a_propos.html', {
        'titre_page': 'À propos',
        'blocs': get_blocs('a_propos'),
        'settings': SiteSettings.get(),
    })


def services(request):
    return render(request, 'core/services.html', {
        'titre_page': 'Services',
        'services': Service.objects.filter(actif=True),
        'blocs': get_blocs('services'),
        'settings': SiteSettings.get(),
    })


def portfolio(request):
    projets = Projet.objects.all()
    demo_projets = [
        {'titre':'E-Commerce Fashion','cat':'Développement Web','desc':"Plateforme e-commerce complète avec plus de 10 000 produits",'img':'https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=800&q=80','tags':['React','Node.js','MongoDB'],'client':'FashionHub'},
        {'titre':'Application Bancaire','cat':'Application Mobile','desc':"Application mobile sécurisée pour la gestion de comptes",'img':'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800&q=80','tags':['React Native','Fintech','Sécurité'],'client':'BankSecure'},
        {'titre':'Dashboard Analytics','cat':'UI/UX Design','desc':"Interface de visualisation de données complexes en temps réel",'img':'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80','tags':['Design System','Data Viz','UX'],'client':'DataFlow'},
        {'titre':'Plateforme SaaS','cat':'Développement Web','desc':"Solution SaaS pour la gestion de projets d'équipes distribuées",'img':'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80','tags':['Vue.js','Python','AWS'],'client':'TeamSync'},
        {'titre':'Application Santé','cat':'Application Mobile','desc':"Application de suivi santé et bien-être avec coach virtuel IA",'img':'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80','tags':['Flutter','IA','Healthcare'],'client':'HealthPlus'},
        {'titre':'Site Corporate','cat':'Développement Web','desc':"Refonte complète du site institutionnel d'un grand groupe",'img':'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80','tags':['Next.js','CMS','SEO'],'client':'GlobalCorp'},
    ]
    return render(request, 'core/portfolio.html', {
        'titre_page': 'Portfolio',
        'projets': projets,
        'demo_projets': demo_projets if not projets.exists() else [],
        'blocs': get_blocs('portfolio'),
        'settings': SiteSettings.get(),
    })


def contact(request):
    """Page Contact — gère GET (formulaire vide) et POST (traitement + envoi email)."""
    if request.method == 'POST':
        formulaire = FormulaireContact(request.POST)
        if formulaire.is_valid():
            # Sauvegarde en base de données
            instance = formulaire.save()

            # Envoi de l'email de notification
            nom = formulaire.cleaned_data.get('nom', '')
            email_client = formulaire.cleaned_data.get('email', '')
            telephone = formulaire.cleaned_data.get('telephone', '')
            entreprise = formulaire.cleaned_data.get('entreprise', '')
            service = formulaire.cleaned_data.get('service_souhaite', '')
            message_client = formulaire.cleaned_data.get('message', '')

            sujet = f"[Nouveau contact] {nom} — {service}"
            corps = f"""
Vous avez reçu une nouvelle demande de contact via votre site web.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DÉTAILS DU CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nom         : {nom}
Email       : {email_client}
Téléphone   : {telephone or 'Non renseigné'}
Entreprise  : {entreprise or 'Non renseignée'}
Service     : {service}

MESSAGE :
{message_client}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Répondre à : {email_client}
"""
            try:
                send_mail(
                    subject=sujet,
                    message=corps,
                    from_email=django_settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[django_settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # L'email n'a pas pu être envoyé mais le message est sauvegardé en BDD
                pass

            messages.success(request, "✅ Message envoyé ! Je vous répondrai sous 24h.")
            return redirect('contact')
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        formulaire = FormulaireContact()

    return render(request, 'core/contact.html', {
        'titre_page': 'Contact',
        'formulaire': formulaire,
        'blocs': get_blocs('contact'),
        'settings': SiteSettings.get(),
    })
def equipe(request):
    return render(request, 'core/equipe.html', {
        'titre_page': 'Notre Équipe',
        'membres': MembreEquipe.objects.filter(actif=True),
        'blocs': get_blocs('equipe'),
        'settings': SiteSettings.get(),
    })