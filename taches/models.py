from django.db import models


class Tache(models.Model):
    """
    Modèle représentant une tâche à accomplir.
    
    Une tâche contient un titre, une description optionnelle, une date de création 
    automatique et un statut de réalisation. Les tâches sont ordonnées par date de 
    création décroissante (les plus récentes en premier).
    
    Attributs:
        titre (CharField): Le titre de la tâche (max 200 caractères).
        description (TextField): Description détaillée de la tâche (optionnel).
        cree_le (DateTimeField): Date et heure de création (automatiquement défini).
        termine (BooleanField): Indicateur de l'accomplissement de la tâche (faux par défaut).
    """
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    termine = models.BooleanField(default=False)

    class Meta:
        ordering = ['-cree_le']

    def __str__(self):
        """
        Retourne la représentation textuelle de la tâche.
        
        Returns:
            str: Le titre de la tâche.
        """
        return self.titre
