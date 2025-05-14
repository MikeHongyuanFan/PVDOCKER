"""
Integration tests for the Asset and Liability APIs.

This test suite covers all CRUD operations for the Asset and Liability APIs,
with different user roles (admin, broker, bd, client) and various test scenarios.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from borrowers.models import Borrower, Guarantor, Asset, Liability
from users.models import User
from tests.integration.factories.user_factory import (
    AdminUserFactory, BrokerUserFactory, UserFactory, ClientUserFactory
)
from tests.integration.factories.borrower_factory import BorrowerFactory
import json
from decimal import Decimal


class AssetLiabilityAPITestBase(APITestCase):
    """Base test class for Asset and Liability API tests."""
    
    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = AdminUserFactory()
        self.broker_user = BrokerUserFactory()
        self.bd_user = UserFactory(role='bd', username='bd_user', email='bd@example.com')
        self.client_user = ClientUserFactory()
        
        # Create borrowers
        self.admin_borrower = BorrowerFactory(
            first_name="Admin",
            last_name="Borrower",
            email="admin.borrower@example.com",
            created_by=self.admin_user
        )
        
        self.broker_borrower = BorrowerFactory(
            first_name="Broker",
            last_name="Borrower",
            email="broker.borrower@example.com",
            created_by=self.broker_user
        )
        
        self.client_borrower = BorrowerFactory(
            first_name="Client",
            last_name="Borrower",
            email="client.borrower@example.com",
            created_by=self.admin_user,
            user=self.client_user
        )
        
        # Create guarantors
        self.admin_guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Admin',
            last_name='Guarantor',
            email='admin.guarantor@example.com',
            borrower=self.admin_borrower,
            created_by=self.admin_user
        )
        
        # Create assets
        self.admin_asset = Asset.objects.create(
            borrower=self.admin_borrower,
            asset_type='property',
            description='Primary residence',
            value=Decimal('500000.00'),
            created_by=self.admin_user
        )
        
        self.broker_asset = Asset.objects.create(
            borrower=self.broker_borrower,
            asset_type='vehicle',
            description='Car',
            value=Decimal('25000.00'),
            created_by=self.broker_user
        )
        
        self.guarantor_asset = Asset.objects.create(
            guarantor=self.admin_guarantor,
            asset_type='savings',
            description='Savings account',
            value=Decimal('50000.00'),
            created_by=self.admin_user
        )
        
        # Create liabilities
        self.admin_liability = Liability.objects.create(
            borrower=self.admin_borrower,
            liability_type='mortgage',
            description='Home loan',
            amount=Decimal('300000.00'),
            monthly_payment=Decimal('1500.00'),
            created_by=self.admin_user
        )
        
        self.broker_liability = Liability.objects.create(
            borrower=self.broker_borrower,
            liability_type='car_loan',
            description='Car loan',
            amount=Decimal('15000.00'),
            monthly_payment=Decimal('500.00'),
            created_by=self.broker_user
        )
        
        self.guarantor_liability = Liability.objects.create(
            guarantor=self.admin_guarantor,
            liability_type='credit_card',
            description='Credit card debt',
            amount=Decimal('5000.00'),
            monthly_payment=Decimal('200.00'),
            created_by=self.admin_user
        )
        
        # Set up API client
        self.client = APIClient()
        
    def get_asset_list_url(self):
        """Get URL for asset list endpoint."""
        return reverse('asset-list')
    
    def get_asset_detail_url(self, asset_id):
        """Get URL for asset detail endpoint."""
        return reverse('asset-detail', kwargs={'pk': asset_id})
    
    def get_liability_list_url(self):
        """Get URL for liability list endpoint."""
        return reverse('liability-list')
    
    def get_liability_detail_url(self, liability_id):
        """Get URL for liability detail endpoint."""
        return reverse('liability-detail', kwargs={'pk': liability_id})


class TestAssetAPI(AssetLiabilityAPITestBase):
    """Test cases for CRUD operations on assets."""
    
    def test_list_assets_admin(self):
        """Test that admin can list all assets."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.get_asset_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all assets
        self.assertTrue(len(response.data) >= 3)
    
    def test_list_assets_broker(self):
        """Test that broker can only list assets they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.get(self.get_asset_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Broker should only see assets they created or have access to
        asset_descriptions = [item['description'] for item in response.data]
        self.assertIn(self.broker_asset.description, asset_descriptions)
        self.assertNotIn(self.admin_asset.description, asset_descriptions)
    
    def test_list_assets_client(self):
        """Test that client can only see assets associated with their borrower profile."""
        self.client.force_authenticate(user=self.client_user)
        
        # Create an asset for the client's borrower profile
        client_asset = Asset.objects.create(
            borrower=self.client_borrower,
            asset_type='investment',
            description='Investment account',
            value=Decimal('10000.00'),
            created_by=self.admin_user
        )
        
        response = self.client.get(self.get_asset_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Client should only see assets associated with their borrower profile
        asset_descriptions = [item['description'] for item in response.data]
        self.assertIn(client_asset.description, asset_descriptions)
        self.assertNotIn(self.admin_asset.description, asset_descriptions)
    
    def test_retrieve_asset_admin(self):
        """Test that admin can retrieve any asset."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Admin can retrieve admin-created asset
        response = self.client.get(self.get_asset_detail_url(self.admin_asset.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.admin_asset.description)
        
        # Admin can retrieve broker-created asset
        response = self.client.get(self.get_asset_detail_url(self.broker_asset.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.broker_asset.description)
    
    def test_retrieve_asset_broker(self):
        """Test that broker can only retrieve assets they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can retrieve their own asset
        response = self.client.get(self.get_asset_detail_url(self.broker_asset.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.broker_asset.description)
        
        # Broker cannot retrieve admin-created asset
        response = self.client.get(self.get_asset_detail_url(self.admin_asset.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_asset_admin(self):
        """Test that admin can create an asset."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'borrower': self.admin_borrower.id,
            'asset_type': 'shares',
            'description': 'Stock portfolio',
            'value': '75000.00'
        }
        
        response = self.client.post(self.get_asset_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify asset was created in database
        self.assertTrue(Asset.objects.filter(description=data['description']).exists())
    
    def test_create_asset_broker(self):
        """Test that broker can create an asset."""
        self.client.force_authenticate(user=self.broker_user)
        
        data = {
            'borrower': self.broker_borrower.id,
            'asset_type': 'investment',
            'description': 'Investment property',
            'value': '350000.00'
        }
        
        response = self.client.post(self.get_asset_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify asset was created in database and linked to broker
        asset = Asset.objects.get(description=data['description'])
        self.assertEqual(asset.created_by, self.broker_user)
    
    def test_create_guarantor_asset(self):
        """Test creating an asset for a guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'guarantor': self.admin_guarantor.id,
            'asset_type': 'property',
            'description': 'Investment property',
            'value': '450000.00'
        }
        
        response = self.client.post(self.get_asset_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify asset was created in database
        self.assertTrue(Asset.objects.filter(description=data['description']).exists())
    
    def test_update_asset_admin(self):
        """Test that admin can update any asset."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'description': 'Updated property',
            'value': '550000.00'
        }
        
        response = self.client.patch(self.get_asset_detail_url(self.admin_asset.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['value'], data['value'])
        
        # Verify asset was updated in database
        self.admin_asset.refresh_from_db()
        self.assertEqual(self.admin_asset.description, data['description'])
        self.assertEqual(str(self.admin_asset.value), data['value'])
    
    def test_update_asset_broker(self):
        """Test that broker can only update assets they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can update their own asset
        data = {
            'description': 'Updated car',
            'value': '30000.00'
        }
        
        response = self.client.patch(self.get_asset_detail_url(self.broker_asset.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['value'], data['value'])
        
        # Broker cannot update admin-created asset
        data = {
            'description': 'Hacked property',
            'value': '1.00'
        }
        
        response = self.client.patch(self.get_asset_detail_url(self.admin_asset.id), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_asset_admin(self):
        """Test that admin can delete any asset."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.get_asset_detail_url(self.admin_asset.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify asset was deleted from database
        self.assertFalse(Asset.objects.filter(id=self.admin_asset.id).exists())
    
    def test_delete_asset_broker(self):
        """Test that broker can only delete assets they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can delete their own asset
        response = self.client.delete(self.get_asset_detail_url(self.broker_asset.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify asset was deleted from database
        self.assertFalse(Asset.objects.filter(id=self.broker_asset.id).exists())
        
        # Broker cannot delete admin-created asset
        response = self.client.delete(self.get_asset_detail_url(self.admin_asset.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Asset.objects.filter(id=self.admin_asset.id).exists())


class TestLiabilityAPI(AssetLiabilityAPITestBase):
    """Test cases for CRUD operations on liabilities."""
    
    def test_list_liabilities_admin(self):
        """Test that admin can list all liabilities."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.get_liability_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all liabilities
        self.assertTrue(len(response.data) >= 3)
    
    def test_list_liabilities_broker(self):
        """Test that broker can only list liabilities they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.get(self.get_liability_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Broker should only see liabilities they created or have access to
        liability_descriptions = [item['description'] for item in response.data]
        self.assertIn(self.broker_liability.description, liability_descriptions)
        self.assertNotIn(self.admin_liability.description, liability_descriptions)
    
    def test_list_liabilities_client(self):
        """Test that client can only see liabilities associated with their borrower profile."""
        self.client.force_authenticate(user=self.client_user)
        
        # Create a liability for the client's borrower profile
        client_liability = Liability.objects.create(
            borrower=self.client_borrower,
            liability_type='personal_loan',
            description='Personal loan',
            amount=Decimal('10000.00'),
            monthly_payment=Decimal('300.00'),
            created_by=self.admin_user
        )
        
        response = self.client.get(self.get_liability_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Client should only see liabilities associated with their borrower profile
        liability_descriptions = [item['description'] for item in response.data]
        self.assertIn(client_liability.description, liability_descriptions)
        self.assertNotIn(self.admin_liability.description, liability_descriptions)
    
    def test_retrieve_liability_admin(self):
        """Test that admin can retrieve any liability."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Admin can retrieve admin-created liability
        response = self.client.get(self.get_liability_detail_url(self.admin_liability.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.admin_liability.description)
        
        # Admin can retrieve broker-created liability
        response = self.client.get(self.get_liability_detail_url(self.broker_liability.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.broker_liability.description)
    
    def test_retrieve_liability_broker(self):
        """Test that broker can only retrieve liabilities they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can retrieve their own liability
        response = self.client.get(self.get_liability_detail_url(self.broker_liability.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.broker_liability.description)
        
        # Broker cannot retrieve admin-created liability
        response = self.client.get(self.get_liability_detail_url(self.admin_liability.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_liability_admin(self):
        """Test that admin can create a liability."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'borrower': self.admin_borrower.id,
            'liability_type': 'personal_loan',
            'description': 'Personal loan',
            'amount': '25000.00',
            'monthly_payment': '500.00'
        }
        
        response = self.client.post(self.get_liability_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify liability was created in database
        self.assertTrue(Liability.objects.filter(description=data['description']).exists())
    
    def test_create_liability_broker(self):
        """Test that broker can create a liability."""
        self.client.force_authenticate(user=self.broker_user)
        
        data = {
            'borrower': self.broker_borrower.id,
            'liability_type': 'credit_card',
            'description': 'Credit card debt',
            'amount': '5000.00',
            'monthly_payment': '200.00'
        }
        
        response = self.client.post(self.get_liability_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify liability was created in database and linked to broker
        liability = Liability.objects.get(description=data['description'])
        self.assertEqual(liability.created_by, self.broker_user)
    
    def test_create_guarantor_liability(self):
        """Test creating a liability for a guarantor."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'guarantor': self.admin_guarantor.id,
            'liability_type': 'mortgage',
            'description': 'Investment property mortgage',
            'amount': '300000.00',
            'monthly_payment': '1500.00'
        }
        
        response = self.client.post(self.get_liability_list_url(), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], data['description'])
        
        # Verify liability was created in database
        self.assertTrue(Liability.objects.filter(description=data['description']).exists())
    
    def test_update_liability_admin(self):
        """Test that admin can update any liability."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'description': 'Updated home loan',
            'amount': '320000.00',
            'monthly_payment': '1600.00'
        }
        
        response = self.client.patch(self.get_liability_detail_url(self.admin_liability.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['amount'], data['amount'])
        self.assertEqual(response.data['monthly_payment'], data['monthly_payment'])
        
        # Verify liability was updated in database
        self.admin_liability.refresh_from_db()
        self.assertEqual(self.admin_liability.description, data['description'])
        self.assertEqual(str(self.admin_liability.amount), data['amount'])
        self.assertEqual(str(self.admin_liability.monthly_payment), data['monthly_payment'])
    
    def test_update_liability_broker(self):
        """Test that broker can only update liabilities they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can update their own liability
        data = {
            'description': 'Updated car loan',
            'amount': '18000.00',
            'monthly_payment': '600.00'
        }
        
        response = self.client.patch(self.get_liability_detail_url(self.broker_liability.id), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['amount'], data['amount'])
        self.assertEqual(response.data['monthly_payment'], data['monthly_payment'])
        
        # Broker cannot update admin-created liability
        data = {
            'description': 'Hacked loan',
            'amount': '1.00'
        }
        
        response = self.client.patch(self.get_liability_detail_url(self.admin_liability.id), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_liability_admin(self):
        """Test that admin can delete any liability."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.get_liability_detail_url(self.admin_liability.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify liability was deleted from database
        self.assertFalse(Liability.objects.filter(id=self.admin_liability.id).exists())
    
    def test_delete_liability_broker(self):
        """Test that broker can only delete liabilities they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can delete their own liability
        response = self.client.delete(self.get_liability_detail_url(self.broker_liability.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify liability was deleted from database
        self.assertFalse(Liability.objects.filter(id=self.broker_liability.id).exists())
        
        # Broker cannot delete admin-created liability
        response = self.client.delete(self.get_liability_detail_url(self.admin_liability.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Liability.objects.filter(id=self.admin_liability.id).exists())