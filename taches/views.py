from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtre les tâches pour ne retourner que celles appartenant à l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les tâches de l'utilisateur connecté.
        """
        return Tache.objects.filter(proprietaire=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associe la tâche créée à l'utilisateur authentifié.
        
        Args:
            serializer: Le sérialiseur contenant les données de la tâche à créer.
        """
        serializer.save(proprietaire=self.request.user)
    
    
