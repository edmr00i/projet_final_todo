from django.shortcuts import render
from .models import Tache


def liste_taches(request):
    """Affiche la liste de toutes les tâches ordonnées par date de création."""
    taches = Tache.objects.all()
    context = {'taches': taches}
    return render(request, 'taches/tache_liste.html', context)
