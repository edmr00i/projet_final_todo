"""
Configuration des URLs principales du projet.

Ce module définit les routes URL au niveau racine du projet Django.
Il inclut les URLs de l'administration Django, l'endpoint d'authentification
par token, les routes de l'API des tâches, et le service du SPA React
(index.html pour toute URL non API/admin/assets).

Routes disponibles:
    - /admin/: Interface d'administration Django
    - /api/token/: Endpoint d'authentification pour obtenir un token (POST)
    - /api/taches/*: Routes de l'API REST pour les tâches (déléguées à taches.urls)
    - /assets/*: Fichiers statiques du build React (JS, CSS)
    - /*: Toute autre URL sert index.html (SPA React)

Pour plus d'informations sur la configuration des URLs Django:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token

# Racine du build React pour servir le SPA
REACT_DIST = settings.BASE_DIR / 'frontend' / 'dist'


def serve_react_index(request, **_kwargs):
    """Sert index.html du build React pour le fallback SPA (routing côté client)."""
    return serve(request, 'index.html', document_root=REACT_DIST)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token),
    path('', include('taches.urls')),  # /api/taches/ via taches.urls
    # Fichiers statiques du build React (JS, CSS)
    path('assets/<path:path>', serve, {'document_root': REACT_DIST / 'assets'}),
    # Favicon et autres fichiers à la racine du build
    path('vite.svg', serve, {'document_root': REACT_DIST, 'path': 'vite.svg'}),
    # Fallback SPA : toute URL non couverte sert index.html
    re_path(r'^.*$', serve_react_index),
]
