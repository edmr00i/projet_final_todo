
from rest_framework.viewsets import ModelViewSet
from .models import Tache
from .serializers import TacheSerializer


class TacheViewSet(ModelViewSet):
    """
    ViewSet pour les opérations CRUD sur les tâches.
    
    Hérite de ModelViewSet de DRF qui gère automatiquement toutes les actions CRUD :
    - list (GET /api/taches/)
    - create (POST /api/taches/)
    - retrieve (GET /api/taches/{id}/)
    - update (PUT /api/taches/{id}/)
    - partial_update (PATCH /api/taches/{id}/)
    - destroy (DELETE /api/taches/{id}/)
    
    Attributs:
        queryset: Toutes les tâches de la base de données.
        serializer_class: Le sérialiseur à utiliser pour la sérialisation/désérialisation.
    """
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
