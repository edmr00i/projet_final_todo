"""
Configuration de l'interface d'administration Django pour le modèle Tache.

Ce module permet de gérer les tâches via l'interface d'administration Django
avec des options de filtrage, recherche et affichage personnalisées.
"""
from django.contrib import admin
from .models import Tache


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration Django pour le modèle Tache.
    
    Personnalise l'affichage et les fonctionnalités de gestion des tâches
    dans l'interface d'administration Django.
    
    Attributs:
        list_display (tuple): Colonnes affichées dans la liste des tâches.
            - titre: Le titre de la tâche
            - termine: Le statut de réalisation
            - cree_le: La date de création
        
        list_filter (tuple): Filtres disponibles dans la barre latérale.
            - termine: Filtre par statut (terminée/en cours)
            - cree_le: Filtre par date de création
        
        search_fields (tuple): Champs utilisables pour la recherche.
            - titre: Recherche dans le titre
            - description: Recherche dans la description
        
        readonly_fields (tuple): Champs en lecture seule dans le formulaire d'édition.
            - cree_le: La date de création ne peut pas être modifiée
    """
    list_display = ('titre', 'termine', 'cree_le')
    list_filter = ('termine', 'cree_le')
    search_fields = ('titre', 'description')
    readonly_fields = ('cree_le',)
