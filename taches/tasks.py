"""
Tâches asynchrones Celery pour l'application taches.

Ce module contient les tâches qui peuvent être exécutées en arrière-plan
de manière asynchrone par Celery, sans bloquer l'interface utilisateur.

Les tâches sont définies avec le décorateur @shared_task, ce qui permet
de les utiliser sans dépendance directe à l'instance de l'application Celery.
"""
import time
from celery import shared_task


@shared_task
def tache_test_asynchrone():
    """
    Tâche de test asynchrone simple.
    
    Cette tâche simule un traitement long en attendant 5 secondes,
    puis affiche un message de succès dans la console du worker Celery.
    
    Utilisation:
        # Exécuter de manière asynchrone (non-bloquant)
        tache_test_asynchrone.delay()
        
        # Exécuter de manière asynchrone et récupérer le résultat
        result = tache_test_asynchrone.apply_async()
        
        # Exécuter de manière synchrone (pour les tests)
        tache_test_asynchrone()
    
    Returns:
        None: Cette tâche n'a pas de valeur de retour.
    
    Notes:
        - Le message s'affiche dans les logs du worker Celery, pas dans le serveur Django.
        - Pour voir le message, assurez-vous que le worker Celery est démarré avec -l info.
    """
    time.sleep(5)
    print("Tâche asynchrone terminée avec succès !")