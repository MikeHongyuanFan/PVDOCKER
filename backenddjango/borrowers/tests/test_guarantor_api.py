"""
Integration tests for the Guarantor API.

This test suite covers all CRUD operations and special endpoints for the Guarantor API,
with different user roles (admin, broker, bd, client) and various test scenarios.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from borrowers.models import Borrower, Guarantor
from users.models import User
from tests.integration.factories.user_factory import (
    AdminUserFactory, BrokerUserFactory, UserFactory, ClientUserFactory
)
from tests.integration.factories.borrower_factory import BorrowerFactory
import json
from decimal import Decimal


class GuarantorAPITestBase(APITestCase):
    """Base test class for Guarantor API tests."""
    
    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = AdminUserFactory()
        self.broker_user = BrokerUserFactory()
        self.bd_user = UserFactory(role='bd', username='bd_user', email='bd@example.com')
        self.client_user = ClientUserFactory()
        self.another_broker = BrokerUserFactory(username='broker2', email='broker2@example.com')
        
        # Create borrowers
        # Admin-created borrower
        self.admin_borrower = BorrowerFactory(
            first_name="Admin",
            last_name="Borrower",
            email="admin.borrower@example.com",
            created_by=self.admin_user
        )
        
        # Broker-created borrower
        self.broker_borrower = BorrowerFactory(
            first_name="Broker",
            last_name="Borrower",
            email="broker.borrower@example.com",
            created_by=self.broker_user
        )
        
        # BD-created borrower
        self.bd_borrower = BorrowerFactory(
            first_name="BD",
            last_name="Borrower",
            email="bd.borrower@example.com",
            created_by=self.bd_user
        )
        
        # Client borrower (linked to client user)
        self.client_borrower = BorrowerFactory(
            first_name="Client",
            last_name="Borrower",
            email="client.borrower@example.com",
            created_by=self.admin_user,
            user=self.client_user
        )
        
        # Create guarantors
        # Admin-created guarantor for admin borrower
        self.admin_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Admin',
            last_name='Guarantor',
            email='admin.guarantor@example.com',
            borrower=self.admin_borrower,
            created_by=self.admin_user
        )
        
        # Broker-created guarantor for broker borrower
        self.broker_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Broker',
            last_name='Guarantor',
            email='broker.guarantor@example.com',
            borrower=self.broker_borrower,
            created_by=self.broker_user
        )
        
        # BD-created guarantor for BD borrower
        self.bd_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='BD',
            last_name='Guarantor',
            email='bd.guarantor@example.com',
            borrower=self.bd_borrower,
            created_by=self.bd_user
        )
        
        # Company guarantor
        self.company_guarantor = Guarantor.objects.create(
            guarantor_type='company',
            company_name='Test Company',
            company_abn='12345678901',
            borrower=self.admin_borrower,
            created_by=self.admin_user
        )
        
        # Set up API client
        self.client = APIClient()
        
    def get_guarantor_list_url(self):
        """Get URL for guarantor list endpoint."""
        return reverse('guarantor-list')
    
    def get_guarantor_detail_url(self, guarantor_id):
        """Get URL for guarantor detail endpoint."""
        return reverse('guarantor-detail', kwargs={'pk': guarantor_id})
    
    def get_guaranteed_applications_url(self, guarantor_id):
        """Get URL for guarantor's guaranteed applications endpoint."""
        return reverse('guarantor-guaranteed-applications', kwargs={'pk': guarantor_id})


class TestGuarantorCRUD(GuarantorAPITestBase):
    """Test cases for CRUD operations on guarantors."""
    
    def test_list_guarantors_admin(self):
        """Test that admin can list all guarantors."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.get_guarantor_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all guarantors
        self.assertTrue(len(response.data) >= 4)
    
    def test_list_guarantors_broker(self):
        """Test that broker can only list their own guarantors."""
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.get(self.get_guarantor_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Broker should only see guarantors they created
        guarantor_emails = [item['email'] for item in response.data if 'email' in item]
        self.assertIn(self.broker_guarantor.email, guarantor_emails)
        self.assertNotIn(self.admin_guarantor.email, guarantor_emails)
    
    def test_list_guarantors_bd(self):
        """Test that BD can only list their own guarantors."""
        self.client.force_authenticate(user=self.bd_user)
        response = self.client.get(self.get_guarantor_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # BD should only see guarantors they created
        guarantor_emails = [item['email'] for item in response.data if 'email' in item]
        self.assertIn(self.bd_guarantor.email, guarantor_emails)
        self.assertNotIn(self.admin_guarantor.email, guarantor_emails)
    
    def test_list_guarantors_client(self):
        """Test that client can only see guarantors associated with their borrower profile."""
        self.client.force_authenticate(user=self.client_user)
        
        # Create a guarantor for the client's borrower profile
        client_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Client',
            last_name='Guarantor',
            email='client.guarantor@example.com',
            borrower=self.client_borrower,
            created_by=self.admin_user
        )
        
        response = self.client.get(self.get_guarantor_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Client should only see guarantors associated with their borrower profile
        guarantor_emails = [item['email'] for item in response.data if 'email' in item]
        self.assertIn(client_guarantor.email, guarantor_emails)
        self.assertNotIn(self.admin_guarantor.email, guarantor_emails)
    
    def test_retrieve_guarantor_admin(self):
        """Test that admin can retrieve any guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Admin can retrieve admin-created guarantor
        response = self.client.get(self.get_guarantor_detail_url(self.admin_guarantor.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.admin_guarantor.email)
        
        # Admin can retrieve broker-created guarantor
        response = self.client.get(self.get_guarantor_detail_url(self.broker_guarantor.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.broker_guarantor.email)
    
    def test_retrieve_guarantor_broker(self):
        """Test that broker can only retrieve their own guarantors."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can retrieve their own guarantor
        response = self.client.get(self.get_guarantor_detail_url(self.broker_guarantor.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.broker_guarantor.email)
        
        # Broker cannot retrieve admin-created guarantor
        response = self.client.get(self.get_guarantor_detail_url(self.admin_guarantor.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_guarantor_admin(self):
        """Test that admin can create a guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'guarantor_type': 'individual',
            'first_name': 'New',
            'last_name': 'Guarantor',
            'email': 'new.guarantor@example.com',
            'mobile': '1234567890',
            'borrower': self.admin_borrower.id
        }
        
        response = self.client.post(self.get_guarantor_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        
        # Verify guarantor was created in database
        self.assertTrue(Guarantor.objects.filter(email=data['email']).exists())
    
    def test_create_guarantor_broker(self):
        """Test that broker can create a guarantor."""
        self.client.force_authenticate(user=self.broker_user)
        
        data = {
            'guarantor_type': 'individual',
            'first_name': 'Broker',
            'last_name': 'New',
            'email': 'broker.new.guarantor@example.com',
            'mobile': '0987654321',
            'borrower': self.broker_borrower.id
        }
        
        response = self.client.post(self.get_guarantor_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        
        # Verify guarantor was created in database and linked to broker
        guarantor = Guarantor.objects.get(email=data['email'])
        self.assertEqual(guarantor.created_by, self.broker_user)
    
    def test_create_company_guarantor(self):
        """Test creating a company guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'guarantor_type': 'company',
            'company_name': 'New Company',
            'company_abn': '98765432109',
            'borrower': self.admin_borrower.id
        }
        
        response = self.client.post(self.get_guarantor_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['company_name'], data['company_name'])
        
        # Verify guarantor was created in database
        self.assertTrue(Guarantor.objects.filter(company_name=data['company_name']).exists())
    
    def test_create_guarantor_validation(self):
        """Test validation when creating guarantors."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Missing required fields for individual guarantor
        data = {
            'guarantor_type': 'individual',
            'email': 'invalid.guarantor@example.com',
            'borrower': self.admin_borrower.id
        }
        
        response = self.client.post(self.get_guarantor_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing required fields for company guarantor
        data = {
            'guarantor_type': 'company',
            'borrower': self.admin_borrower.id
        }
        
        response = self.client.post(self.get_guarantor_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_guarantor_admin(self):
        """Test that admin can update any guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'first_name': 'Updated',
            'email': 'updated.admin.guarantor@example.com'
        }
        
        response = self.client.patch(self.get_guarantor_detail_url(self.admin_guarantor.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['email'], data['email'])
        
        # Verify guarantor was updated in database
        self.admin_guarantor.refresh_from_db()
        self.assertEqual(self.admin_guarantor.first_name, data['first_name'])
        self.assertEqual(self.admin_guarantor.email, data['email'])
    
    def test_update_guarantor_broker(self):
        """Test that broker can only update their own guarantors."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can update their own guarantor
        data = {
            'first_name': 'Updated',
            'email': 'updated.broker.guarantor@example.com'
        }
        
        response = self.client.patch(self.get_guarantor_detail_url(self.broker_guarantor.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['email'], data['email'])
        
        # Broker cannot update admin-created guarantor
        data = {
            'first_name': 'Hacked',
            'email': 'hacked@example.com'
        }
        
        response = self.client.patch(self.get_guarantor_detail_url(self.admin_guarantor.id), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_guarantor_admin(self):
        """Test that admin can delete any guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.get_guarantor_detail_url(self.admin_guarantor.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify guarantor was deleted from database
        self.assertFalse(Guarantor.objects.filter(id=self.admin_guarantor.id).exists())
    
    def test_delete_guarantor_broker(self):
        """Test that broker can only delete their own guarantors."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can delete their own guarantor
        response = self.client.delete(self.get_guarantor_detail_url(self.broker_guarantor.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify guarantor was deleted from database
        self.assertFalse(Guarantor.objects.filter(id=self.broker_guarantor.id).exists())
        
        # Broker cannot delete admin-created guarantor
        response = self.client.delete(self.get_guarantor_detail_url(self.admin_guarantor.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Guarantor.objects.filter(id=self.admin_guarantor.id).exists())


class TestGuarantorSpecialEndpoints(GuarantorAPITestBase):
    """Test cases for special endpoints of the Guarantor API."""
    
    def test_guaranteed_applications_endpoint(self):
        """Test the guaranteed applications endpoint."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Get guaranteed applications for a guarantor
        url = self.get_guaranteed_applications_url(self.admin_guarantor.id)
        response = self.client.get(url)
        
        # Since we don't have actual applications in the test setup,
        # we just check that the endpoint returns a 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_unauthorized_access_to_special_endpoints(self):
        """Test unauthorized access to special endpoints."""
        # No authentication
        url = self.get_guaranteed_applications_url(self.admin_guarantor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_broker_access_to_special_endpoints(self):
        """Test broker access to special endpoints."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can access their own guarantor's special endpoints
        url = self.get_guaranteed_applications_url(self.broker_guarantor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Broker cannot access admin guarantor's special endpoints
        url = self.get_guaranteed_applications_url(self.admin_guarantor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_client_access_to_special_endpoints(self):
        """Test client access to special endpoints."""
        self.client.force_authenticate(user=self.client_user)
        
        # Create a guarantor for the client's borrower profile
        client_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Client',
            last_name='Guarantor',
            email='client.guarantor@example.com',
            borrower=self.client_borrower,
            created_by=self.admin_user
        )
        
        # Client can access their own guarantor's special endpoints
        url = self.get_guaranteed_applications_url(client_guarantor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Client cannot access admin guarantor's special endpoints
        url = self.get_guaranteed_applications_url(self.admin_guarantor.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)