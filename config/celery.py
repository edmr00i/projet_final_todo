"""
Configuration de Celery pour le projet de gestion de tâches.

Ce module configure Celery pour qu'il fonctionne en harmonie avec Django.
Il initialise l'application Celery, la configure pour utiliser les paramètres Django,
et active l'autodécouverte automatique des fichiers tasks.py dans toutes les applications
Django installées.

Celery permet d'exécuter des tâches en arrière-plan de manière asynchrone, sans bloquer
l'interface utilisateur. Les tâches sont envoyées à un broker de messages (Redis) et
exécutées par des workers Celery.

Pour plus d'informations:
    https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""
import os
from celery import Celery

# Définir le module de configuration Django par défaut pour Celery
# Cela permet à Celery de charger les paramètres depuis settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Créer l'instance de l'application Celery
# Le nom 'config' identifie cette application Celery
app = Celery('config')

# Configuration de Celery à partir des paramètres Django
# - namespace='CELERY' : tous les paramètres Celery dans settings.py doivent commencer par CELERY_
# - Les paramètres sont chargés depuis le fichier settings.py de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodécouverte des tâches Celery
# Celery va automatiquement chercher et charger les fichiers tasks.py
# dans toutes les applications listées dans INSTALLED_APPS de Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Tâche de débogage pour vérifier que Celery fonctionne correctement.
    
    Cette tâche peut être appelée pour tester la configuration de Celery.
    Elle affiche simplement la requête reçue dans les logs du worker.
    
    Args:
        self: Référence à la tâche elle-même (bind=True permet d'accéder au contexte).
    
    Utilisation:
        from config.celery import debug_task
        debug_task.delay()
    """
    print(f'Request: {self.request!r}')