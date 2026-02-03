from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tache
from .forms import TacheForm


def liste_taches(request):
    """Affiche la liste de toutes les tâches ordonnées par date de création."""
    taches = Tache.objects.all()
    context = {'taches': taches}
    return render(request, 'taches/tache_liste.html', context)


def ajouter_tache(request):
    """Crée une nouvelle tâche via un formulaire."""
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tâche ajoutée avec succès!')
            return redirect('liste_taches')
    else:
        form = TacheForm()
    
    context = {'form': form, 'titre_page': 'Ajouter une tâche'}
    return render(request, 'taches/tache_form.html', context)
