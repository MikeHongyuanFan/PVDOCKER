from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from borrowers.models import Asset, Borrower, Guarantor
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class AssetAPITest(TestCase):
    """Test the Asset API endpoints"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a company borrower
        self.company_borrower = Borrower.objects.create(
            is_company=True,
            company_name="Test Company",
            company_abn="12345678901",
            company_acn="123456789",
            created_by=self.user
        )
        
        # Create a guarantor
        self.guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name="Test",
            last_name="Guarantor",
            created_by=self.user
        )
        
        # Create a client for API requests
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_company_asset(self):
        """Test creating a company asset through the API"""
        # This test assumes you have an API endpoint for creating company assets
        # If not, you'll need to create one or modify this test
        
        url = reverse('borrower-assets', args=[self.company_borrower.id])
        data = {
            'asset_type': 'Property',
            'description': 'Office Building',
            'value': '1000000.00',
            'amount_owing': '500000.00',
            'to_be_refinanced': True,
            'address': '123 Business St, City'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, 201)
        
        # Check that the asset was created correctly
        asset = Asset.objects.get(id=response.data['id'])
        self.assertEqual(asset.borrower, self.company_borrower)
        self.assertEqual(asset.asset_type, 'Property')
        self.assertEqual(float(asset.value), 1000000.00)
        self.assertEqual(float(asset.amount_owing), 500000.00)
        self.assertTrue(asset.to_be_refinanced)
        self.assertIsNone(asset.bg_type)
    
    def test_create_guarantor_asset(self):
        """Test creating a guarantor asset through the API"""
        # This test assumes you have an API endpoint for creating guarantor assets
        # If not, you'll need to create one or modify this test
        
        url = reverse('guarantor-assets', args=[self.guarantor.id])
        data = {
            'asset_type': 'Property',
            'description': 'Residential Home',
            'value': '750000.00',
            'amount_owing': '400000.00',
            'address': '456 Home St, Suburb',
            'bg_type': 'BG1'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, 201)
        
        # Check that the asset was created correctly
        asset = Asset.objects.get(id=response.data['id'])
        self.assertEqual(asset.guarantor, self.guarantor)
        self.assertEqual(asset.asset_type, 'Property')
        self.assertEqual(float(asset.value), 750000.00)
        self.assertEqual(float(asset.amount_owing), 400000.00)
        self.assertEqual(asset.bg_type, 'BG1')
        self.assertFalse(asset.to_be_refinanced)
    
    def test_create_guarantor_asset_without_bg_type(self):
        """Test creating a guarantor asset without bg_type (should fail)"""
        url = reverse('guarantor-assets', args=[self.guarantor.id])
        data = {
            'asset_type': 'Property',
            'description': 'Residential Home',
            'value': '750000.00',
            'amount_owing': '400000.00',
            'address': '456 Home St, Suburb'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check that the request failed
        self.assertEqual(response.status_code, 400)
        self.assertIn('bg_type', response.data)
    
    def test_create_company_asset_with_bg_type(self):
        """Test creating a company asset with bg_type (should be ignored)"""
        url = reverse('borrower-assets', args=[self.company_borrower.id])
        data = {
            'asset_type': 'Property',
            'description': 'Office Building',
            'value': '1000000.00',
            'amount_owing': '500000.00',
            'to_be_refinanced': True,
            'address': '123 Business St, City',
            'bg_type': 'BG1'  # This should be ignored
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, 201)
        
        # Check that the asset was created correctly with bg_type set to None
        asset = Asset.objects.get(id=response.data['id'])
        self.assertIsNone(asset.bg_type)
