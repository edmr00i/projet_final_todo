from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from celery.result import AsyncResult
from .models import Tache
from .serializers import TacheSerializer
from .tasks import tache_test_asynchrone, send_creation_email, generate_task_report


class TacheViewSet(ModelViewSet):
    """
    ViewSet pour les opÃ©rations CRUD sur les tÃ¢ches.
    
    HÃ©rite de ModelViewSet de DRF qui gÃ¨re automatiquement toutes les actions CRUD.
    Toutes les opÃ©rations nÃ©cessitent une authentification par token et ne retournent
    que les tÃ¢ches appartenant Ã  l'utilisateur authentifiÃ©.
    
    Endpoints disponibles:
        - list (GET /api/taches/): Liste toutes les tÃ¢ches de l'utilisateur connectÃ©.
        - create (POST /api/taches/): CrÃ©e une nouvelle tÃ¢che pour l'utilisateur connectÃ©.
        - retrieve (GET /api/taches/{id}/): RÃ©cupÃ¨re une tÃ¢che spÃ©cifique par ID.
        - update (PUT /api/taches/{id}/): Met Ã  jour complÃ¨tement une tÃ¢che.
        - partial_update (PATCH /api/taches/{id}/): Met Ã  jour partiellement une tÃ¢che.
        - destroy (DELETE /api/taches/{id}/): Supprime une tÃ¢che.
    
    Attributs:
        serializer_class (TacheSerializer): Le sÃ©rialiseur utilisÃ© pour la sÃ©rialisation/dÃ©sÃ©rialisation.
        permission_classes (list): Liste des classes de permission (IsAuthenticated requis).
    
    MÃ©thodes:
        get_queryset(): Filtre les tÃ¢ches pour ne retourner que celles de l'utilisateur connectÃ©.
        perform_create(serializer): Associe automatiquement la tÃ¢che crÃ©Ã©e Ã  l'utilisateur authentifiÃ©
                                    et dÃ©clenche l'envoi d'e-mail asynchrone.
    """
    serializer_class = TacheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtre les tÃ¢ches pour ne retourner que celles appartenant Ã  l'utilisateur authentifiÃ©.
        
        Cette mÃ©thode garantit que chaque utilisateur ne voit et ne peut modifier
        que ses propres tÃ¢ches, assurant l'isolation des donnÃ©es entre utilisateurs.
        
        Returns:
            QuerySet: Un QuerySet filtrÃ© contenant uniquement les tÃ¢ches de l'utilisateur connectÃ©,
                     ordonnÃ©es par date de crÃ©ation dÃ©croissante.
        """
        return Tache.objects.filter(proprietaire=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associe automatiquement la tÃ¢che crÃ©Ã©e Ã  l'utilisateur authentifiÃ©
        et dÃ©clenche l'envoi d'un e-mail de notification en arriÃ¨re-plan.
        
        Cette mÃ©thode est appelÃ©e lors de la crÃ©ation d'une nouvelle tÃ¢che via POST.
        Elle garantit que le champ 'proprietaire' est automatiquement dÃ©fini avec
        l'utilisateur actuellement authentifiÃ©, sans nÃ©cessiter de le passer dans les donnÃ©es.
        
        AprÃ¨s la sauvegarde, une tÃ¢che Celery asynchrone est dÃ©clenchÃ©e pour envoyer
        un e-mail de notification, sans bloquer la rÃ©ponse HTTP au client.
        
        Args:
            serializer (TacheSerializer): Le sÃ©rialiseur contenant les donnÃ©es de la tÃ¢che Ã  crÃ©er.
                Les donnÃ©es doivent contenir au minimum 'titre'. 'description' et 'termine' sont optionnels.
        
        Flow:
            1. Sauvegarde de la tÃ¢che avec l'utilisateur comme propriÃ©taire
            2. DÃ©clenchement asynchrone de send_creation_email avec l'ID de la tÃ¢che
            3. Retour immÃ©diat au client (pas d'attente de l'envoi d'e-mail)
        """
        # Sauvegarder la tÃ¢che avec le propriÃ©taire
        serializer.save(proprietaire=self.request.user)
        
        # DÃ©clencher l'envoi d'e-mail de maniÃ¨re asynchrone
        send_creation_email.delay(serializer.instance.id)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def test_celery_view(request):
    """
    Vue de test pour vÃ©rifier que Celery fonctionne correctement.
    
    Cette vue dÃ©clenche la tÃ¢che asynchrone tache_test_asynchrone en arriÃ¨re-plan
    et retourne immÃ©diatement une rÃ©ponse au client sans attendre la fin de la tÃ¢che.
    
    Endpoint:
        GET ou POST /api/test-celery/
    
    Permissions:
        - NÃ©cessite une authentification par token
    
    Returns:
        Response: Un message JSON confirmant que la tÃ¢che a Ã©tÃ© lancÃ©e en arriÃ¨re-plan.
            La rÃ©ponse est immÃ©diate (non-bloquante), mÃªme si la tÃ¢che prend 5 secondes.
    
    Exemple de rÃ©ponse:
        {
            "message": "TÃ¢che asynchrone lancÃ©e en arriÃ¨re-plan !",
            "task_id": "abc123-def456-..."
        }
    
    Notes:
        - La tÃ¢che s'exÃ©cute dans un worker Celery sÃ©parÃ©
        - Le message "TÃ¢che asynchrone terminÃ©e avec succÃ¨s !" apparaÃ®tra dans les logs du worker
        - Cette vue dÃ©montre le principe du traitement asynchrone : l'utilisateur n'attend pas
    """
    # DÃ©clencher la tÃ¢che de maniÃ¨re asynchrone
    result = tache_test_asynchrone.delay()
    
    return Response({
        'message': 'TÃ¢che asynchrone lancÃ©e en arriÃ¨re-plan !',
        'task_id': str(result.id)
    }, status=status.HTTP_200_OK)


class StartReportGenerationView(APIView):
    """
    Vue API pour démarrer la génération d'un rapport de tâches de manière asynchrone.
    
    Cette vue déclenche la tâche Celery generate_task_report en arrière-plan
    et retourne immédiatement l'ID de la tâche au client pour permettre le suivi.
    
    Endpoint:
        POST /api/start-report/
    
    Permissions:
        - Nécessite une authentification par token
    
    Returns:
        Response: Un objet JSON contenant l'ID de la tâche lancée.
            Status 202 ACCEPTED indique que la tâche a été acceptée et est en cours.
    
    Exemple de réponse:
        {
            "task_id": "abc123-def456-789ghi",
            "message": "Génération du rapport lancée en arrière-plan"
        }
    
    Notes:
        - La réponse est immédiate (non-bloquante)
        - L'ID de la tâche peut être utilisé pour interroger l'état via CheckTaskStatusView
        - La tâche prend 15 secondes à s'exécuter complètement
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Déclenche la génération asynchrone du rapport.
        
        Args:
            request: L'objet HttpRequest
        
        Returns:
            Response: JSON avec task_id et message de confirmation
        """
        # Déclencher la tâche de génération de rapport
        result = generate_task_report.delay()
        
        return Response({
            'task_id': result.id,
            'message': 'Génération du rapport lancée en arrière-plan'
        }, status=status.HTTP_202_ACCEPTED)


class CheckTaskStatusView(APIView):
    """
    Vue API pour vérifier l'état d'une tâche Celery en cours d'exécution.
    
    Cette vue permet de suivre la progression d'une tâche asynchrone en interrogeant
    son statut via son ID. Elle utilise AsyncResult de Celery pour récupérer
    l'état actuel et le résultat (si disponible) de la tâche.
    
    Endpoint:
        GET /api/check-report-status/<task_id>/
    
    Permissions:
        - Nécessite une authentification par token
    
    Args:
        task_id (str): L'identifiant unique de la tâche Celery (UUID)
    
    Returns:
        Response: Un objet JSON contenant l'état et le résultat de la tâche.
    
    États possibles:
        - PENDING: La tâche est en attente d'exécution
        - STARTED: La tâche a démarré son exécution
        - SUCCESS: La tâche s'est terminée avec succès
        - FAILURE: La tâche a échoué
        - RETRY: La tâche est en cours de nouvelle tentative
        - REVOKED: La tâche a été annulée
    
    Exemple de réponse (en cours):
        {
            "task_id": "abc123-def456-789ghi",
            "state": "STARTED",
            "result": null
        }
    
    Exemple de réponse (terminée):
        {
            "task_id": "abc123-def456-789ghi",
            "state": "SUCCESS",
            "result": "Le rapport de tâches a été généré avec succès !"
        }
    
    Exemple de réponse (échec):
        {
            "task_id": "abc123-def456-789ghi",
            "state": "FAILURE",
            "result": "Error message..."
        }
    
    Notes:
        - Cette vue peut être appelée régulièrement (polling) depuis le frontend
        - Le client doit stocker le task_id reçu de StartReportGenerationView
        - En production, considérer WebSockets pour des mises à jour en temps réel
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id):
        """
        Récupère l'état actuel de la tâche.
        
        Args:
            request: L'objet HttpRequest
            task_id (str): L'ID de la tâche Celery
        
        Returns:
            Response: JSON avec task_id, state et result
        """
        # Récupérer l'objet AsyncResult pour cette tâche
        task_result = AsyncResult(task_id)
        
        # Préparer la réponse avec l'état et le résultat
        response_data = {
            'task_id': task_id,
            'state': task_result.state,
            'result': None
        }
        
        # Si la tâche est terminée avec succès, inclure le résultat
        if task_result.state == 'SUCCESS':
            response_data['result'] = task_result.result
        # Si la tâche a échoué, inclure l'erreur
        elif task_result.state == 'FAILURE':
            response_data['result'] = str(task_result.info)
        
        return Response(response_data, status=status.HTTP_200_OK)