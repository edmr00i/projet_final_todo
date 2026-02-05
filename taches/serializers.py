from rest_framework import serializers
from .models import Tache


class TacheSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Tache.
    
    Gère la conversion entre les instances du modèle Tache et les représentations JSON
    pour l'API REST. Expose tous les champs du modèle avec des règles spécifiques
    pour certains champs.
    
    Champs sérialisés:
        - id (int, lecture seule): Identifiant unique de la tâche.
        - titre (str): Titre de la tâche (max 200 caractères, requis).
        - description (str): Description détaillée de la tâche (optionnel, peut être vide).
        - cree_le (datetime, lecture seule): Date et heure de création au format ISO 8601.
        - termine (bool): Statut de réalisation de la tâche (False par défaut).
        - proprietaire (str, lecture seule): Nom d'utilisateur du propriétaire de la tâche.
    
    Notes:
        - Le champ 'proprietaire' est en lecture seule et affiche le nom d'utilisateur.
        - Le champ 'proprietaire' ne peut pas être modifié via l'API (géré automatiquement par le ViewSet).
        - Les champs 'id' et 'cree_le' sont automatiquement générés et en lecture seule.
    """
    proprietaire = serializers.ReadOnlyField(source='proprietaire.username')
    
    class Meta:
        model = Tache
        fields = '__all__'
