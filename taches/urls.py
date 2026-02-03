from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Création du router et enregistrement du ViewSet
router = DefaultRouter()
router.register(r'taches', views.TacheViewSet, basename='tache')

urlpatterns = [
    path('api/', include(router.urls)),
]