"""
Configuration des URLs pour l'application taches.

Ce module définit les routes de l'API REST pour la gestion des tâches.
Utilise le DefaultRouter de Django REST Framework pour générer automatiquement
les routes CRUD à partir du TacheViewSet, et ajoute une route de test pour Celery.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Création du router et enregistrement du ViewSet
router = DefaultRouter()
router.register(r'taches', views.TacheViewSet, basename='tache')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/test-celery/', views.test_celery_view, name='test-celery'),
]