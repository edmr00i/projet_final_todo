from django.shortcuts import render, redirect, get_object_or_404
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


def modifier_tache(request, tache_id):
    """Modifie une tâche existante via un formulaire."""
    tache = get_object_or_404(Tache, pk=tache_id)
    
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tâche modifiée avec succès!')
            return redirect('liste_taches')
    else:
        form = TacheForm(instance=tache)
    
    context = {'form': form, 'titre_page': 'Modifier une tâche'}
    return render(request, 'taches/tache_form.html', context)


def supprimer_tache(request, tache_id):
    """Supprime une tâche après confirmation."""
    tache = get_object_or_404(Tache, pk=tache_id)
    
    if request.method == 'POST':
        tache.delete()
        messages.success(request, 'Tâche supprimée avec succès!')
        return redirect('liste_taches')
    
    context = {'tache': tache}
    return render(request, 'taches/tache_confirm_delete.html', context)
