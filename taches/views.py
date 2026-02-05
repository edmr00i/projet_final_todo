from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Tache
from .serializers import TacheSerializer
from .tasks import tache_test_asynchrone, send_creation_email


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
        perform_create(serializer): Associe automatiquement la tâche créée à l'utilisateur authentifié
                                    et déclenche l'envoi d'e-mail asynchrone.
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
        Associe automatiquement la tâche créée à l'utilisateur authentifié
        et déclenche l'envoi d'un e-mail de notification en arrière-plan.
        
        Cette méthode est appelée lors de la création d'une nouvelle tâche via POST.
        Elle garantit que le champ 'proprietaire' est automatiquement défini avec
        l'utilisateur actuellement authentifié, sans nécessiter de le passer dans les données.
        
        Après la sauvegarde, une tâche Celery asynchrone est déclenchée pour envoyer
        un e-mail de notification, sans bloquer la réponse HTTP au client.
        
        Args:
            serializer (TacheSerializer): Le sérialiseur contenant les données de la tâche à créer.
                Les données doivent contenir au minimum 'titre'. 'description' et 'termine' sont optionnels.
        
        Flow:
            1. Sauvegarde de la tâche avec l'utilisateur comme propriétaire
            2. Déclenchement asynchrone de send_creation_email avec l'ID de la tâche
            3. Retour immédiat au client (pas d'attente de l'envoi d'e-mail)
        """
        # Sauvegarder la tâche avec le propriétaire
        serializer.save(proprietaire=self.request.user)
        
        # Déclencher l'envoi d'e-mail de manière asynchrone
        send_creation_email.delay(serializer.instance.id)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def test_celery_view(request):
    """
    Vue de test pour vérifier que Celery fonctionne correctement.
    
    Cette vue déclenche la tâche asynchrone tache_test_asynchrone en arrière-plan
    et retourne immédiatement une réponse au client sans attendre la fin de la tâche.
    
    Endpoint:
        GET ou POST /api/test-celery/
    
    Permissions:
        - Nécessite une authentification par token
    
    Returns:
        Response: Un message JSON confirmant que la tâche a été lancée en arrière-plan.
            La réponse est immédiate (non-bloquante), même si la tâche prend 5 secondes.
    
    Exemple de réponse:
        {
            "message": "Tâche asynchrone lancée en arrière-plan !",
            "task_id": "abc123-def456-..."
        }
    
    Notes:
        - La tâche s'exécute dans un worker Celery séparé
        - Le message "Tâche asynchrone terminée avec succès !" apparaîtra dans les logs du worker
        - Cette vue démontre le principe du traitement asynchrone : l'utilisateur n'attend pas
    """
    # Déclencher la tâche de manière asynchrone
    result = tache_test_asynchrone.delay()
    
    return Response({
        'message': 'Tâche asynchrone lancée en arrière-plan !',
        'task_id': str(result.id)
    }, status=status.HTTP_200_OK)