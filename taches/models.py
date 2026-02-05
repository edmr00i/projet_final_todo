from django.db import models
from django.conf import settings

class Tache(models.Model):
    """
    Modèle représentant une tâche à accomplir.
    
    Une tâche contient un titre, une description optionnelle, une date de création 
    automatique et un statut de réalisation. Chaque tâche appartient à un utilisateur
    (proprietaire) et les tâches sont ordonnées par date de création décroissante 
    (les plus récentes en premier).
    
    Attributs:
        titre (CharField): Le titre de la tâche (max 200 caractères, requis).
        description (TextField): Description détaillée de la tâche (optionnel, peut être vide).
        cree_le (DateTimeField): Date et heure de création (automatiquement défini à la création).
        termine (BooleanField): Indicateur de l'accomplissement de la tâche (faux par défaut).
        proprietaire (ForeignKey): Référence vers l'utilisateur propriétaire de la tâche.
            Suppression en cascade si l'utilisateur est supprimé.
    
    Relations:
        - proprietaire: Relation ForeignKey vers AUTH_USER_MODEL avec related_name='taches'.
    
    Métadonnées:
        - ordering: Les tâches sont triées par date de création décroissante ('-cree_le').
    """
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    termine = models.BooleanField(default=False)
    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='taches'
    )

    class Meta:
        ordering = ['-cree_le']

    def __str__(self):
        """
        Retourne la représentation textuelle de la tâche.
        
        Utilisé pour l'affichage dans l'interface d'administration Django
        et dans les représentations de débogage.
        
        Returns:
            str: Le titre de la tâche.
        """
        return self.titre
