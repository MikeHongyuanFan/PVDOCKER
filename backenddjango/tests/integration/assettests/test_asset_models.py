from django.test import TestCase
from django.core.exceptions import ValidationError
from borrowers.models import Asset, Borrower, Guarantor
from django.contrib.auth import get_user_model

User = get_user_model()

class AssetModelTest(TestCase):
    """Test the Asset model"""
    
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
    
    def test_company_asset_creation(self):
        """Test creating a valid company asset"""
        asset = Asset(
            borrower=self.company_borrower,
            asset_type="Property",
            description="Office Building",
            value=1000000.00,
            amount_owing=500000.00,
            to_be_refinanced=True,
            address="123 Business St, City",
            created_by=self.user
        )
        
        # Should not raise any validation errors
        asset.clean()
        asset.save()
        
        self.assertEqual(asset.borrower, self.company_borrower)
        self.assertEqual(asset.asset_type, "Property")
        self.assertEqual(asset.value, 1000000.00)
        self.assertEqual(asset.amount_owing, 500000.00)
        self.assertTrue(asset.to_be_refinanced)
        self.assertIsNone(asset.bg_type)
    
    def test_guarantor_asset_creation(self):
        """Test creating a valid guarantor asset"""
        asset = Asset(
            guarantor=self.guarantor,
            asset_type="Property",
            description="Residential Home",
            value=750000.00,
            amount_owing=400000.00,
            address="456 Home St, Suburb",
            bg_type="BG1",
            created_by=self.user
        )
        
        # Should not raise any validation errors
        asset.clean()
        asset.save()
        
        self.assertEqual(asset.guarantor, self.guarantor)
        self.assertEqual(asset.asset_type, "Property")
        self.assertEqual(asset.value, 750000.00)
        self.assertEqual(asset.amount_owing, 400000.00)
        self.assertEqual(asset.bg_type, "BG1")
        self.assertFalse(asset.to_be_refinanced)
    
    def test_guarantor_asset_without_bg_type(self):
        """Test creating a guarantor asset without bg_type should fail"""
        asset = Asset(
            guarantor=self.guarantor,
            asset_type="Property",
            description="Residential Home",
            value=750000.00,
            amount_owing=400000.00,
            address="456 Home St, Suburb",
            created_by=self.user
        )
        
        # Should raise a validation error
        with self.assertRaises(ValidationError):
            asset.clean()
    
    def test_company_asset_with_bg_type(self):
        """Test creating a company asset with bg_type should fail"""
        asset = Asset(
            borrower=self.company_borrower,
            asset_type="Property",
            description="Office Building",
            value=1000000.00,
            amount_owing=500000.00,
            address="123 Business St, City",
            bg_type="BG1",  # This should cause validation to fail
            created_by=self.user
        )
        
        # Should raise a validation error
        with self.assertRaises(ValidationError):
            asset.clean()
    
    def test_guarantor_asset_with_to_be_refinanced(self):
        """Test creating a guarantor asset with to_be_refinanced should fail"""
        asset = Asset(
            guarantor=self.guarantor,
            asset_type="Property",
            description="Residential Home",
            value=750000.00,
            amount_owing=400000.00,
            address="456 Home St, Suburb",
            bg_type="BG1",
            to_be_refinanced=True,  # This should cause validation to fail
            created_by=self.user
        )
        
        # Should raise a validation error
        with self.assertRaises(ValidationError):
            asset.clean()
