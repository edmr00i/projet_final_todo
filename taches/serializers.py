from rest_framework import serializers
from .models import Tache


class TacheSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Tache.
    
    Expose tous les champs du modèle Tache pour la sérialisation/désérialisation
    des données JSON.
    """
    proprietaire = serializers.ReadOnlyField(source='proprietaire.username')
    
    class Meta:
        model = Tache
        fields = '__all__'
