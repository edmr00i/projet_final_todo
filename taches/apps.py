"""
Configuration de l'application Django 'taches'.

Ce module définit la configuration de l'application Django pour la gestion
des tâches, incluant le nom de l'application et d'éventuelles configurations
spécifiques à l'application.
"""
from django.apps import AppConfig


class TachesConfig(AppConfig):
    """
    Configuration de l'application 'taches'.
    
    Cette classe définit les paramètres de configuration pour l'application
    de gestion des tâches, notamment son nom utilisé par Django pour
    l'identifier dans INSTALLED_APPS.
    
    Attributs:
        name (str): Nom de l'application ('taches').
    """
    name = 'taches'
