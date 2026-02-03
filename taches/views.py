from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tache
from .forms import TacheForm


def liste_taches(request):
    """
    Affiche la liste de toutes les tâches.
    
    Récupère l'ensemble des tâches de la base de données, ordonnées par date de 
    création décroissante, et les affiche dans un template.
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
    
    Returns:
        HttpResponse: La réponse rendue du template tache_liste.html avec le contexte.
    """
    taches = Tache.objects.all()
    context = {'taches': taches}
    return render(request, 'taches/tache_liste.html', context)


def ajouter_tache(request):
    """
    Affiche un formulaire pour créer une nouvelle tâche.
    
    En GET, affiche le formulaire vierge. En POST, traite la soumission du formulaire,
    sauvegarde la tâche en base de données et redirige vers la liste des tâches.
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
    
    Returns:
        HttpResponse: En GET, retourne le template tache_form.html avec le formulaire vierge.
                     En POST valide, redirige vers la liste des tâches (liste_taches).
    """
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
    """
    Affiche un formulaire pour modifier une tâche existante.
    
    En GET, affiche le formulaire pré-rempli avec les données de la tâche.
    En POST, traite la soumission, met à jour la tâche en base de données et 
    redirige vers la liste des tâches. Retourne une erreur 404 si la tâche n'existe pas.
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
        tache_id (int): L'identifiant unique de la tâche à modifier.
    
    Returns:
        HttpResponse: En GET, retourne le template tache_form.html avec le formulaire pré-rempli.
                     En POST valide, redirige vers la liste des tâches (liste_taches).
        HttpResponse: Erreur 404 si la tâche avec l'ID spécifié n'existe pas.
    """
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
    """
    Affiche une page de confirmation avant de supprimer une tâche.
    
    En GET, affiche un template de confirmation avec les détails de la tâche.
    En POST, supprime effectivement la tâche de la base de données et redirige 
    vers la liste. Retourne une erreur 404 si la tâche n'existe pas.
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
        tache_id (int): L'identifiant unique de la tâche à supprimer.
    
    Returns:
        HttpResponse: En GET, retourne le template tache_confirm_delete.html avec 
                     les détails de la tâche à supprimer.
                     En POST, redirige vers la liste des tâches (liste_taches).
        HttpResponse: Erreur 404 si la tâche avec l'ID spécifié n'existe pas.
    """
    tache = get_object_or_404(Tache, pk=tache_id)
    
    if request.method == 'POST':
        tache.delete()
        messages.success(request, 'Tâche supprimée avec succès!')
        return redirect('liste_taches')
    
    context = {'tache': tache}
    return render(request, 'taches/tache_confirm_delete.html', context)
