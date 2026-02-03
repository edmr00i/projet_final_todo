from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_taches, name='liste_taches'),
    path('ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('modifier/<int:tache_id>/', views.modifier_tache, name='modifier_tache'),
    # path('supprimer/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
    # path('basculer_termine/<int:tache_id>/', views.basculer_termine, name='basculer_termine'),
]