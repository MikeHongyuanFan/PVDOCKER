"""
Integration tests for the Director API.

This test suite covers all CRUD operations for the Director API,
with different user roles (admin, broker, bd, client) and various test scenarios.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from borrowers.models import Borrower, Director
from users.models import User
from tests.integration.factories.user_factory import (
    AdminUserFactory, BrokerUserFactory, UserFactory, ClientUserFactory
)
from tests.integration.factories.borrower_factory import CompanyBorrowerFactory
import json
from decimal import Decimal


class DirectorAPITestBase(APITestCase):
    """Base test class for Director API tests."""
    
    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = AdminUserFactory()
        self.broker_user = BrokerUserFactory()
        self.bd_user = UserFactory(role='bd', username='bd_user', email='bd@example.com')
        self.client_user = ClientUserFactory()
        
        # Create company borrowers
        self.admin_company = CompanyBorrowerFactory(
            company_name="Admin Company",
            email="admin.company@example.com",
            created_by=self.admin_user
        )
        
        self.broker_company = CompanyBorrowerFactory(
            company_name="Broker Company",
            email="broker.company@example.com",
            created_by=self.broker_user
        )
        
        # Create directors
        self.admin_director1 = Director.objects.create(
            borrower=self.admin_company,
            name="John Smith",
            roles="director,shareholder",
            director_id="DIR001",
            created_by=self.admin_user
        )
        
        self.admin_director2 = Director.objects.create(
            borrower=self.admin_company,
            name="Jane Doe",
            roles="secretary",
            director_id="DIR002",
            created_by=self.admin_user
        )
        
        self.broker_director = Director.objects.create(
            borrower=self.broker_company,
            name="Bob Johnson",
            roles="director",
            director_id="DIR003",
            created_by=self.broker_user
        )
        
        # Set up API client
        self.client = APIClient()
        
    def get_director_list_url(self):
        """Get URL for director list endpoint."""
        return reverse('director-list')
    
    def get_director_detail_url(self, director_id):
        """Get URL for director detail endpoint."""
        return reverse('director-detail', kwargs={'pk': director_id})


class TestDirectorAPI(DirectorAPITestBase):
    """Test cases for CRUD operations on directors."""
    
    def test_list_directors_admin(self):
        """Test that admin can list all directors."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.get_director_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all directors
        self.assertTrue(len(response.data) >= 3)
        director_names = [item['name'] for item in response.data]
        self.assertIn(self.admin_director1.name, director_names)
        self.assertIn(self.admin_director2.name, director_names)
        self.assertIn(self.broker_director.name, director_names)
    
    def test_list_directors_broker(self):
        """Test that broker can only list directors they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.get(self.get_director_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Broker should only see directors they created or have access to
        director_names = [item['name'] for item in response.data]
        self.assertIn(self.broker_director.name, director_names)
        self.assertNotIn(self.admin_director1.name, director_names)
        self.assertNotIn(self.admin_director2.name, director_names)
    
    def test_retrieve_director_admin(self):
        """Test that admin can retrieve any director."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Admin can retrieve admin-created director
        response = self.client.get(self.get_director_detail_url(self.admin_director1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.admin_director1.name)
        
        # Admin can retrieve broker-created director
        response = self.client.get(self.get_director_detail_url(self.broker_director.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.broker_director.name)
    
    def test_retrieve_director_broker(self):
        """Test that broker can only retrieve directors they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can retrieve their own director
        response = self.client.get(self.get_director_detail_url(self.broker_director.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.broker_director.name)
        
        # Broker cannot retrieve admin-created director
        response = self.client.get(self.get_director_detail_url(self.admin_director1.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_director_admin(self):
        """Test that admin can create a director."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'borrower': self.admin_company.id,
            'name': 'New Director',
            'roles': 'director,public_officer',
            'director_id': 'DIR004'
        }
        
        response = self.client.post(self.get_director_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['roles'], data['roles'])
        
        # Verify director was created in database
        self.assertTrue(Director.objects.filter(name=data['name']).exists())
    
    def test_create_director_broker(self):
        """Test that broker can create a director."""
        self.client.force_authenticate(user=self.broker_user)
        
        data = {
            'borrower': self.broker_company.id,
            'name': 'Broker New Director',
            'roles': 'director,shareholder',
            'director_id': 'DIR005'
        }
        
        response = self.client.post(self.get_director_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['roles'], data['roles'])
        
        # Verify director was created in database and linked to broker
        director = Director.objects.get(name=data['name'])
        self.assertEqual(director.created_by, self.broker_user)
    
    def test_update_director_admin(self):
        """Test that admin can update any director."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'name': 'Updated Director Name',
            'roles': 'director,secretary,shareholder'
        }
        
        response = self.client.patch(self.get_director_detail_url(self.admin_director1.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['roles'], data['roles'])
        
        # Verify director was updated in database
        self.admin_director1.refresh_from_db()
        self.assertEqual(self.admin_director1.name, data['name'])
        self.assertEqual(self.admin_director1.roles, data['roles'])
    
    def test_update_director_broker(self):
        """Test that broker can only update directors they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can update their own director
        data = {
            'name': 'Updated Broker Director',
            'roles': 'director,secretary'
        }
        
        response = self.client.patch(self.get_director_detail_url(self.broker_director.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['roles'], data['roles'])
        
        # Broker cannot update admin-created director
        data = {
            'name': 'Hacked Director',
            'roles': 'hacker'
        }
        
        response = self.client.patch(self.get_director_detail_url(self.admin_director1.id), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_director_admin(self):
        """Test that admin can delete any director."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.get_director_detail_url(self.admin_director1.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify director was deleted from database
        self.assertFalse(Director.objects.filter(id=self.admin_director1.id).exists())
    
    def test_delete_director_broker(self):
        """Test that broker can only delete directors they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can delete their own director
        response = self.client.delete(self.get_director_detail_url(self.broker_director.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify director was deleted from database
        self.assertFalse(Director.objects.filter(id=self.broker_director.id).exists())
        
        # Broker cannot delete admin-created director
        response = self.client.delete(self.get_director_detail_url(self.admin_director1.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Director.objects.filter(id=self.admin_director1.id).exists())
    
    def test_unauthorized_access(self):
        """Test unauthorized access to director endpoints."""
        # No authentication
        response = self.client.get(self.get_director_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(self.get_director_detail_url(self.admin_director1.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        data = {
            'borrower': self.admin_company.id,
            'name': 'Unauthorized Director',
            'roles': 'director'
        }
        
        response = self.client.post(self.get_director_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)