from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_taches, name='liste_taches'),
    path('ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('modifier/<int:tache_id>/', views.modifier_tache, name='modifier_tache'),
    path('supprimer/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
    path('api/liste/', views.TacheListCreateAPIView.as_view(), name='liste_taches_api'),
    path('api/detail/<int:pk>/', views.TacheRetrieveUpdateDestroyAPIView.as_view(), name='detail_tache_api'),
]