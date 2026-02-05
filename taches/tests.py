"""
Tests unitaires pour l'application taches.

Ce module contient tous les tests pour vérifier le bon fonctionnement
du modèle Tache, du sérialiseur TacheSerializer, et du ViewSet TacheViewSet.
"""
import time
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Tache
from .serializers import TacheSerializer

User = get_user_model()


class TacheModelTest(TestCase):
    """Tests unitaires pour le modèle Tache."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_creation_tache(self):
        """Test la création d'une tâche avec tous les champs."""
        tache = Tache.objects.create(
            titre='Tâche de test',
            description='Description de test',
            termine=False,
            proprietaire=self.user
        )
        self.assertEqual(tache.titre, 'Tâche de test')
        self.assertEqual(tache.description, 'Description de test')
        self.assertFalse(tache.termine)
        self.assertEqual(tache.proprietaire, self.user)
        self.assertIsNotNone(tache.cree_le)
        self.assertIsNotNone(tache.id)

    def test_creation_tache_sans_description(self):
        """Test la création d'une tâche sans description."""
        tache = Tache.objects.create(
            titre='Tâche sans description',
            proprietaire=self.user
        )
        self.assertEqual(tache.titre, 'Tâche sans description')
        self.assertEqual(tache.description, '')
        self.assertFalse(tache.termine)

    def test_tache_terminee_par_defaut(self):
        """Test que le statut 'termine' est False par défaut."""
        tache = Tache.objects.create(
            titre='Tâche test',
            proprietaire=self.user
        )
        self.assertFalse(tache.termine)

    def test_str_representation(self):
        """Test la représentation textuelle de la tâche."""
        tache = Tache.objects.create(
            titre='Ma tâche',
            proprietaire=self.user
        )
        self.assertEqual(str(tache), 'Ma tâche')

    def test_ordering_par_date_decroissante(self):
        """Test que les tâches sont ordonnées par date de création décroissante."""
        tache1 = Tache.objects.create(
            titre='Première tâche',
            proprietaire=self.user
        )
        time.sleep(0.01)  # Délai pour garantir des dates différentes
        tache2 = Tache.objects.create(
            titre='Deuxième tâche',
            proprietaire=self.user
        )
        time.sleep(0.01)  # Délai pour garantir des dates différentes
        tache3 = Tache.objects.create(
            titre='Troisième tâche',
            proprietaire=self.user
        )
        
        taches = list(Tache.objects.all())
        self.assertEqual(taches[0], tache3)
        self.assertEqual(taches[1], tache2)
        self.assertEqual(taches[2], tache1)

    def test_relation_proprietaire(self):
        """Test la relation ForeignKey avec l'utilisateur."""
        tache = Tache.objects.create(
            titre='Tâche test',
            proprietaire=self.user
        )
        self.assertEqual(tache.proprietaire, self.user)
        self.assertIn(tache, self.user.taches.all())

    def test_suppression_cascade_utilisateur(self):
        """Test que la suppression d'un utilisateur supprime ses tâches."""
        tache = Tache.objects.create(
            titre='Tâche à supprimer',
            proprietaire=self.user
        )
        tache_id = tache.id
        
        self.user.delete()
        
        self.assertFalse(Tache.objects.filter(id=tache_id).exists())


class TacheSerializerTest(TestCase):
    """Tests unitaires pour le sérialiseur TacheSerializer."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tache = Tache.objects.create(
            titre='Tâche de test',
            description='Description de test',
            termine=False,
            proprietaire=self.user
        )

    def test_serialisation_complete(self):
        """Test la sérialisation complète d'une tâche."""
        serializer = TacheSerializer(self.tache)
        data = serializer.data
        
        self.assertEqual(data['titre'], 'Tâche de test')
        self.assertEqual(data['description'], 'Description de test')
        self.assertFalse(data['termine'])
        self.assertEqual(data['proprietaire'], 'testuser')
        self.assertIn('id', data)
        self.assertIn('cree_le', data)

    def test_deserialisation_creation(self):
        """Test la désérialisation pour créer une nouvelle tâche."""
        data = {
            'titre': 'Nouvelle tâche',
            'description': 'Nouvelle description',
            'termine': True
        }
        serializer = TacheSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        tache = serializer.save(proprietaire=self.user)
        self.assertEqual(tache.titre, 'Nouvelle tâche')
        self.assertEqual(tache.description, 'Nouvelle description')
        self.assertTrue(tache.termine)
        self.assertEqual(tache.proprietaire, self.user)

    def test_deserialisation_sans_description(self):
        """Test la désérialisation sans description."""
        data = {
            'titre': 'Tâche sans description',
            'termine': False
        }
        serializer = TacheSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        tache = serializer.save(proprietaire=self.user)
        self.assertEqual(tache.titre, 'Tâche sans description')
        self.assertEqual(tache.description, '')

    def test_proprietaire_readonly(self):
        """Test que le champ proprietaire est en lecture seule."""
        data = {
            'titre': 'Tâche test',
            'proprietaire': 'autreuser'
        }
        serializer = TacheSerializer(data=data)
        # Le champ proprietaire ne devrait pas être dans les données validées
        # car il est géré par le ViewSet
        self.assertTrue(serializer.is_valid())

    def test_validation_titre_requis(self):
        """Test que le titre est requis."""
        data = {
            'description': 'Description sans titre'
        }
        serializer = TacheSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titre', serializer.errors)


class TacheViewSetTest(APITestCase):
    """Tests unitaires pour le ViewSet TacheViewSet."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.client = APIClient()
        
        # Créer des tâches pour chaque utilisateur
        self.tache_user1 = Tache.objects.create(
            titre='Tâche user1',
            description='Description user1',
            proprietaire=self.user1
        )
        self.tache_user2 = Tache.objects.create(
            titre='Tâche user2',
            description='Description user2',
            proprietaire=self.user2
        )

    def test_list_taches_authentifie(self):
        """Test la liste des tâches pour un utilisateur authentifié."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titre'], 'Tâche user1')
        self.assertEqual(response.data[0]['id'], self.tache_user1.id)

    def test_list_taches_non_authentifie(self):
        """Test que la liste nécessite une authentification."""
        url = reverse('tache-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_isolation_donnees_utilisateurs(self):
        """Test que chaque utilisateur ne voit que ses propres tâches."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.tache_user1.id)
        
        # Vérifier que user2 ne voit pas les tâches de user1
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.tache_user2.id)

    def test_create_tache(self):
        """Test la création d'une nouvelle tâche."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        data = {
            'titre': 'Nouvelle tâche',
            'description': 'Nouvelle description',
            'termine': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['titre'], 'Nouvelle tâche')
        self.assertEqual(response.data['proprietaire'], 'user1')
        self.assertEqual(Tache.objects.filter(proprietaire=self.user1).count(), 2)

    def test_create_tache_sans_description(self):
        """Test la création d'une tâche sans description."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        data = {
            'titre': 'Tâche sans description'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['titre'], 'Tâche sans description')
        self.assertEqual(response.data['description'], '')

    def test_create_tache_auto_assigne_proprietaire(self):
        """Test que le propriétaire est automatiquement assigné lors de la création."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        data = {
            'titre': 'Tâche test'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['proprietaire'], 'user1')
        
        tache = Tache.objects.get(id=response.data['id'])
        self.assertEqual(tache.proprietaire, self.user1)

    def test_retrieve_tache(self):
        """Test la récupération d'une tâche spécifique."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], 'Tâche user1')
        self.assertEqual(response.data['id'], self.tache_user1.id)

    def test_retrieve_tache_autre_utilisateur(self):
        """Test qu'un utilisateur ne peut pas récupérer les tâches d'un autre."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user2.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_tache_complete(self):
        """Test la mise à jour complète d'une tâche (PUT)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user1.id})
        data = {
            'titre': 'Titre modifié',
            'description': 'Description modifiée',
            'termine': True
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], 'Titre modifié')
        self.assertEqual(response.data['description'], 'Description modifiée')
        self.assertTrue(response.data['termine'])
        
        self.tache_user1.refresh_from_db()
        self.assertEqual(self.tache_user1.titre, 'Titre modifié')
        self.assertTrue(self.tache_user1.termine)

    def test_partial_update_tache(self):
        """Test la mise à jour partielle d'une tâche (PATCH)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user1.id})
        data = {
            'termine': True
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['termine'])
        self.assertEqual(response.data['titre'], 'Tâche user1')  # Non modifié
        
        self.tache_user1.refresh_from_db()
        self.assertTrue(self.tache_user1.termine)

    def test_update_tache_autre_utilisateur(self):
        """Test qu'un utilisateur ne peut pas modifier les tâches d'un autre."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user2.id})
        data = {
            'titre': 'Tentative de modification'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_tache(self):
        """Test la suppression d'une tâche."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tache.objects.filter(id=self.tache_user1.id).exists())

    def test_delete_tache_autre_utilisateur(self):
        """Test qu'un utilisateur ne peut pas supprimer les tâches d'un autre."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-detail', kwargs={'pk': self.tache_user2.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tache.objects.filter(id=self.tache_user2.id).exists())

    def test_create_tache_titre_requis(self):
        """Test que le titre est requis lors de la création."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        data = {
            'description': 'Description sans titre'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('titre', response.data)

    def test_ordering_liste_taches(self):
        """Test que les tâches sont ordonnées par date décroissante."""
        # Créer plusieurs tâches pour user1 avec des délais pour garantir des dates différentes
        time.sleep(0.01)  # Délai pour s'assurer que les nouvelles tâches sont après self.tache_user1
        tache1 = Tache.objects.create(
            titre='Tâche 1',
            proprietaire=self.user1
        )
        time.sleep(0.01)  # Délai pour garantir des dates différentes
        tache2 = Tache.objects.create(
            titre='Tâche 2',
            proprietaire=self.user1
        )
        time.sleep(0.01)  # Délai pour garantir des dates différentes
        tache3 = Tache.objects.create(
            titre='Tâche 3',
            proprietaire=self.user1
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('tache-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifier l'ordre (les plus récentes en premier)
        ids = [t['id'] for t in response.data]
        self.assertEqual(ids[0], tache3.id)
        self.assertEqual(ids[1], tache2.id)
        self.assertEqual(ids[2], tache1.id)
        self.assertEqual(ids[3], self.tache_user1.id)