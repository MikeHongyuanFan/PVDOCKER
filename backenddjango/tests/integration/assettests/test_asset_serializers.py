from django.test import TestCase
from rest_framework.test import APIRequestFactory
from borrowers.models import Asset, Borrower, Guarantor
from applications.serializers_asset import GuarantorAssetSerializer, CompanyAssetSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class AssetSerializerTest(TestCase):
    """Test the Asset serializers"""
    
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
        
        # Create a factory for API requests
        self.factory = APIRequestFactory()
    
    def test_company_asset_serializer_valid(self):
        """Test the CompanyAssetSerializer with valid data"""
        data = {
            'asset_type': 'Property',
            'description': 'Office Building',
            'value': '1000000.00',
            'amount_owing': '500000.00',
            'to_be_refinanced': True,
            'address': '123 Business St, City'
        }
        
        serializer = CompanyAssetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Check that bg_type is set to None
        self.assertIsNone(serializer.validated_data.get('bg_type'))
    
    def test_company_asset_serializer_with_bg_type(self):
        """Test the CompanyAssetSerializer with bg_type (should be removed)"""
        data = {
            'asset_type': 'Property',
            'description': 'Office Building',
            'value': '1000000.00',
            'amount_owing': '500000.00',
            'to_be_refinanced': True,
            'address': '123 Business St, City',
            'bg_type': 'BG1'  # This should be removed by the serializer
        }
        
        serializer = CompanyAssetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Check that bg_type is set to None
        self.assertIsNone(serializer.validated_data.get('bg_type'))
    
    def test_guarantor_asset_serializer_valid(self):
        """Test the GuarantorAssetSerializer with valid data"""
        data = {
            'asset_type': 'Property',
            'description': 'Residential Home',
            'value': '750000.00',
            'amount_owing': '400000.00',
            'address': '456 Home St, Suburb',
            'bg_type': 'BG1'
        }
        
        serializer = GuarantorAssetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Check that to_be_refinanced is set to False
        self.assertFalse(serializer.validated_data.get('to_be_refinanced'))
    
    def test_guarantor_asset_serializer_without_bg_type(self):
        """Test the GuarantorAssetSerializer without bg_type (should fail)"""
        data = {
            'asset_type': 'Property',
            'description': 'Residential Home',
            'value': '750000.00',
            'amount_owing': '400000.00',
            'address': '456 Home St, Suburb'
        }
        
        serializer = GuarantorAssetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('bg_type', serializer.errors)
    
    def test_guarantor_asset_serializer_with_to_be_refinanced(self):
        """Test the GuarantorAssetSerializer with to_be_refinanced (should be removed)"""
        data = {
            'asset_type': 'Property',
            'description': 'Residential Home',
            'value': '750000.00',
            'amount_owing': '400000.00',
            'address': '456 Home St, Suburb',
            'bg_type': 'BG1',
            'to_be_refinanced': True  # This should be set to False by the serializer
        }
        
        serializer = GuarantorAssetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Check that to_be_refinanced is set to False
        self.assertFalse(serializer.validated_data.get('to_be_refinanced'))
