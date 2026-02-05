from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Tache
from .serializers import TacheSerializer


class TacheViewSet(ModelViewSet):
    """
    ViewSet pour les opérations CRUD sur les tâches.
    
    Hérite de ModelViewSet de DRF qui gère automatiquement toutes les actions CRUD.
    Toutes les opérations nécessitent une authentification par token et ne retournent
    que les tâches appartenant à l'utilisateur authentifié.
    
    Endpoints disponibles:
        - list (GET /api/taches/): Liste toutes les tâches de l'utilisateur connecté.
        - create (POST /api/taches/): Crée une nouvelle tâche pour l'utilisateur connecté.
        - retrieve (GET /api/taches/{id}/): Récupère une tâche spécifique par ID.
        - update (PUT /api/taches/{id}/): Met à jour complètement une tâche.
        - partial_update (PATCH /api/taches/{id}/): Met à jour partiellement une tâche.
        - destroy (DELETE /api/taches/{id}/): Supprime une tâche.
    
    Attributs:
        serializer_class (TacheSerializer): Le sérialiseur utilisé pour la sérialisation/désérialisation.
        permission_classes (list): Liste des classes de permission (IsAuthenticated requis).
    
    Méthodes:
        get_queryset(): Filtre les tâches pour ne retourner que celles de l'utilisateur connecté.
        perform_create(serializer): Associe automatiquement la tâche créée à l'utilisateur authentifié.
    """
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtre les tâches pour ne retourner que celles appartenant à l'utilisateur authentifié.
        
        Cette méthode garantit que chaque utilisateur ne voit et ne peut modifier
        que ses propres tâches, assurant l'isolation des données entre utilisateurs.
        
        Returns:
            QuerySet: Un QuerySet filtré contenant uniquement les tâches de l'utilisateur connecté,
                     ordonnées par date de création décroissante.
        """
        return Tache.objects.filter(proprietaire=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associe automatiquement la tâche créée à l'utilisateur authentifié.
        
        Cette méthode est appelée lors de la création d'une nouvelle tâche via POST.
        Elle garantit que le champ 'proprietaire' est automatiquement défini avec
        l'utilisateur actuellement authentifié, sans nécessiter de le passer dans les données.
        
        Args:
            serializer (TacheSerializer): Le sérialiseur contenant les données de la tâche à créer.
                Les données doivent contenir au minimum 'titre'. 'description' et 'termine' sont optionnels.
        """
        serializer.save(proprietaire=self.request.user)
    
    
