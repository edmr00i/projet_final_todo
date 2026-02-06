"""
Tâches asynchrones Celery pour l'application taches.

Ce module contient les tâches qui peuvent être exécutées en arrière-plan
de manière asynchrone par Celery, sans bloquer l'interface utilisateur.

Les tâches sont définies avec le décorateur @shared_task, ce qui permet
de les utiliser sans dépendance directe à l'instance de l'application Celery.
"""
import time
from celery import shared_task
from django.core.mail import send_mail
from .models import Tache

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


@shared_task
def send_creation_email(tache_id):
    """
    Envoie un e-mail de notification lors de la création d'une tâche.
    
    Cette tâche asynchrone envoie un e-mail à l'administrateur pour notifier
    la création d'une nouvelle tâche. L'e-mail est envoyé en arrière-plan
    sans bloquer la réponse API à l'utilisateur.
    
    Args:
        tache_id (int): L'identifiant de la tâche qui vient d'être créée.
    
    Utilisation:
        # Exécuter de manière asynchrone (non-bloquant)
        send_creation_email.delay(tache_id)
        
        # Exécuter de manière asynchrone avec gestion du résultat
        result = send_creation_email.apply_async(args=[tache_id])
    
    Returns:
        str: Un message de confirmation de l'envoi de l'e-mail.
    
    Raises:
        Tache.DoesNotExist: Si aucune tâche ne correspond à l'ID fourni.
    
    Notes:
        - En développement, l'e-mail s'affiche dans la console du serveur Django.
        - En production, configurez EMAIL_BACKEND pour utiliser un vrai serveur SMTP.
        - L'adresse 'admin@example.com' est factice et doit être remplacée en production.
    """
    try:
        # Récupérer la tâche depuis la base de données
        tache = Tache.objects.get(id=tache_id)
        
        # Construire le sujet et le message de l'e-mail
        sujet = f"Nouvelle tâche créée : {tache.titre}"
        message = f"""
Bonjour,

Une nouvelle tâche vient d'être créée :

Titre : {tache.titre}
Description : {tache.description or 'Aucune description'}
Créée par : {tache.proprietaire.username}
Date de création : {tache.cree_le.strftime('%d/%m/%Y à %H:%M')}
Statut : {'Terminée' if tache.termine else 'En cours'}

Cordialement,
L'équipe de gestion de tâches
        """
        
        # Envoyer l'e-mail
        send_mail(
            subject=sujet,
            message=message,
            from_email='noreply@taches.com',
            recipient_list=['admin@example.com'],
            fail_silently=False,
        )
        
        return f"E-mail envoyé avec succès pour la tâche #{tache_id}"
        
    except Tache.DoesNotExist:
        return f"Erreur : Aucune tâche trouvée avec l'ID {tache_id}"


@shared_task
def generate_task_report():
    """
    Génère un rapport de tâches de manière asynchrone.
    
    Cette tâche simule un traitement long (analyse, calculs, génération de PDF, etc.)
    en attendant 15 secondes avant de retourner un message de succès.
    
    Elle peut être utilisée pour démontrer le suivi de progression d'une tâche
    asynchrone depuis l'interface utilisateur React.
    
    Utilisation:
        # Exécuter de manière asynchrone (non-bloquant)
        result = generate_task_report.delay()
        
        # Récupérer l'ID de la tâche pour le suivi
        task_id = result.id
        
        # Vérifier le statut plus tard
        from celery.result import AsyncResult
        task_result = AsyncResult(task_id)
        if task_result.ready():
            print(task_result.result)
    
    Returns:
        str: Un message de confirmation de génération du rapport.
    
    Notes:
        - Le traitement prend 15 secondes (simulation d'un long traitement)
        - En production, cette tâche pourrait générer un vrai rapport PDF,
          analyser des données, effectuer des calculs complexes, etc.
        - L'utilisateur peut suivre la progression via l'ID de la tâche retourné
    """
    # Simuler un traitement long
    time.sleep(15)
    
    # Retourner le message de succès
    return "Le rapport de tâches a été généré avec succès !"


@shared_task
def cleanup_completed_tasks():
    """
    Supprime toutes les tâches marquées comme terminées.
    
    Cette tâche asynchrone recherche toutes les tâches avec termine=True
    et les supprime de la base de données. Utile pour le nettoyage
    périodique des tâches complétées.
    
    Utilisation:
        # Exécuter de manière asynchrone (non-bloquant)
        result = cleanup_completed_tasks.delay()
        
        # Exécuter de manière synchrone (pour les tests)
        count = cleanup_completed_tasks()
        
        # Planifier avec Celery Beat (exemple dans settings.py)
        # CELERY_BEAT_SCHEDULE = {
        #     'cleanup-completed-tasks-weekly': {
        #         'task': 'taches.tasks.cleanup_completed_tasks',
        #         'schedule': crontab(hour=0, minute=0, day_of_week='sunday'),
        #     },
        # }
    
    Returns:
        int: Le nombre de tâches supprimées.
    
    Notes:
        - Cette action est irréversible.
        - En production, envisagez d'archiver les tâches plutôt que de les supprimer.
    """
    # Récupérer et supprimer toutes les tâches terminées
    taches_terminees = Tache.objects.filter(termine=True)
    count = taches_terminees.count()
    taches_terminees.delete()
    
    return count