from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tache
from .forms import TacheForm
from .serializers import TacheSerializer


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


@api_view(['GET', 'POST'])
def liste_taches_api(request):
    """
    Retourne la liste de toutes les tâches au format JSON ou crée une nouvelle tâche.
    
    Vue basée sur une fonction utilisant le décorateur @api_view de DRF.
    
    GET: Accepte les requêtes GET et retourne toutes les tâches.
    POST: Accepte les requêtes POST pour créer une nouvelle tâche.
         - Valide les données avec TacheSerializer
         - Si valides: sauvegarde la tâche et retourne un statut 201 Created
         - Si invalides: retourne les erreurs avec un statut 400
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
    
    Returns:
        Response: 
            - GET: Réponse DRF contenant les données sérialisées de toutes les tâches.
            - POST (valide): Données de la tâche créée avec statut 201.
            - POST (invalide): Erreurs de validation avec statut 400.
    """
    if request.method == 'GET':
        taches = Tache.objects.all()
        serializer = TacheSerializer(taches, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_tache_api(request, pk):
    """
    Récupère, met à jour ou supprime une tâche spécifique par sa clé primaire.
    
    Vue basée sur une fonction utilisant le décorateur @api_view de DRF.
    
    GET: Récupère les détails d'une tâche.
    PUT: Met à jour complètement une tâche.
         - Valide les données avec TacheSerializer
         - Si valides: met à jour la tâche et retourne les données avec statut 200
         - Si invalides: retourne les erreurs avec statut 400
    DELETE: Supprime une tâche.
            - Supprime la tâche et retourne un statut 204 No Content
            - Retourne une erreur 404 si la tâche n'existe pas
    
    Args:
        request (HttpRequest): L'objet requête HTTP.
        pk (int): La clé primaire (id) de la tâche.
    
    Returns:
        Response:
            - GET: Données sérialisées de la tâche avec statut 200.
            - PUT (valide): Données mises à jour de la tâche avec statut 200.
            - PUT (invalide): Erreurs de validation avec statut 400.
            - DELETE: Statut 204 No Content si succès.
            - 404: Si la tâche n'existe pas.
    """
    try:
        tache = Tache.objects.get(pk=pk)
    except Tache.DoesNotExist:
        return Response(
            {'detail': 'Tâche non trouvée.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = TacheSerializer(tache)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TacheSerializer(tache, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        tache.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

