"""
Formulaires Django pour le modèle Tache.

Ce module définit les formulaires utilisés pour créer et modifier des tâches
via l'interface web Django (non utilisés par l'API REST).
"""
from django import forms
from .models import Tache


class TacheForm(forms.ModelForm):
    """
    Formulaire Django pour créer et modifier des tâches.
    
    Formulaire basé sur le modèle Tache avec des widgets personnalisés
    pour améliorer l'expérience utilisateur dans les templates Django.
    
    Champs:
        - titre (TextInput): Titre de la tâche avec placeholder.
        - description (Textarea): Description optionnelle avec placeholder et 4 lignes par défaut.
        - termine (CheckboxInput): Case à cocher pour marquer la tâche comme terminée.
    
    Note:
        Le champ 'proprietaire' n'est pas inclus dans le formulaire car il est
        géré automatiquement par la vue lors de la création.
    """
    class Meta:
        model = Tache
        fields = ['titre', 'description', 'termine']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de la tâche'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description (optionnel)', 'rows': 4}),
            'termine': forms.CheckboxInput(),
        }
