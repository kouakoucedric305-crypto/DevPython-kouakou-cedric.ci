"""Formulaires Django pour l'application core."""
from django import forms
from .models import MessageContact

class FormulaireContact(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ['nom', 'email', 'entreprise', 'telephone', 'service_souhaite', 'message']
        widgets = {
            'nom':      forms.TextInput(attrs={'class':'form-control','placeholder':'Jean Dupont'}),
            'email':    forms.EmailInput(attrs={'class':'form-control','placeholder':'jean@entreprise.fr'}),
            'entreprise': forms.TextInput(attrs={'class':'form-control','placeholder':"Nom de l'entreprise"}),
            'telephone':forms.TextInput(attrs={'class':'form-control','placeholder':'+33 1 23 45 67 89'}),
            'service_souhaite': forms.Select(attrs={'class':'form-control'}),
            'message':  forms.Textarea(attrs={'class':'form-control','placeholder':'Décrivez votre projet...','rows':6}),
        }
        labels = {
            'nom':'Nom complet *', 'email':'Email *',
            'entreprise':'Entreprise', 'telephone':'Téléphone',
            'service_souhaite':'Service souhaité *', 'message':'Message *',
        }

    def clean_message(self):
        msg = self.cleaned_data.get('message','')
        if len(msg) < 10:
            raise forms.ValidationError("Le message doit contenir au moins 10 caractères.")
        return msg
