from django import forms
from .models import Tache


class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['titre', 'description', 'termine']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de la tâche'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description (optionnel)', 'rows': 4}),
            'termine': forms.CheckboxInput(),
        }
