import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from applications.models import Application, SecurityProperty
from borrowers.models import Borrower, Guarantor
from brokers.models import BDM, Branch
from products.models import Product
from datetime import date, timedelta

User = get_user_model()

class EnhancedApplicationsEndpointTests(TestCase):
    """
    Integration tests for the enhanced applications endpoint
    """
    
    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a test branch
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='456 Branch Ave',
            created_by=self.user
        )
        
        # Create a test BDM
        self.bdm = BDM.objects.create(
            name='John Manager',
            email='bdm@example.com',
            phone='0987654321',
            branch=self.branch,
            created_by=self.user
        )
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Loan Product',
            created_by=self.user
        )
        
        # Create test borrowers
        self.individual_borrower = Borrower.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            phone='1122334455',
            date_of_birth='1980-01-01',
            residential_address='789 Resident St',
            created_by=self.user
        )
        
        self.company_borrower = Borrower.objects.create(
            is_company=True,
            company_name='ABC Company',
            company_abn='12345678901',
            company_acn='123456789',
            contact_number='5566778899',
            created_by=self.user
        )
        
        # Create a test guarantor
        self.guarantor = Guarantor.objects.create(
            first_name='Bob',
            last_name='Smith',
            email='bob@example.com',
            mobile='9988776655',
            date_of_birth='1975-05-15',
            created_by=self.user
        )
        
        # Create test applications
        self.application1 = Application.objects.create(
            reference_number='APP-001',
            loan_amount=Decimal('100000'),
            loan_term=24,
            interest_rate=Decimal('5.5'),
            purpose='Business expansion',
            loan_purpose='Expanding business operations',
            application_type='commercial',
            product_id=self.product.id,
            estimated_settlement_date=date.today() + timedelta(days=30),
            stage='inquiry',
            bd_id=self.bdm.id,
            branch_id=self.branch.id,
            created_by=self.user
        )
        
        # Add borrowers to application
        self.application1.borrowers.add(self.individual_borrower)
        
        # Add guarantor to application
        self.application1.guarantors.add(self.guarantor)
        
        # Create security property
        self.security_property = SecurityProperty.objects.create(
            application=self.application1,
            address_unit='Unit 1',
            address_street_no='123',
            address_street_name='Main St',
            address_suburb='Sydney',
            address_state='NSW',
            address_postcode='2000',
            property_type='residential',
            estimated_value=Decimal('500000'),
            created_by=self.user
        )
        
        # Create a second application with company borrower
        self.application2 = Application.objects.create(
            reference_number='APP-002',
            loan_amount=Decimal('250000'),
            loan_term=36,
            interest_rate=Decimal('6.0'),
            purpose='Property purchase',
            loan_purpose='Purchasing commercial property',
            application_type='commercial',
            product_id=self.product.id,
            estimated_settlement_date=date.today() + timedelta(days=45),
            stage='assessment',
            security_address='456 Security Blvd, Melbourne VIC 3000',
            bd_id=self.bdm.id,
            branch_id=self.branch.id,
            created_by=self.user
        )
        
        # Add company borrower to second application
        self.application2.borrowers.add(self.company_borrower)
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URL for the enhanced applications endpoint
        self.url = reverse('enhanced-application-list')
    
    def test_enhanced_applications_endpoint_returns_correct_fields(self):
        """Test that the enhanced applications endpoint returns all required fields"""
        response = self.client.get(self.url)
        
        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected number of applications
        self.assertEqual(response.data['count'], 2)
        
        # Get the first application from the results
        app1 = next((app for app in response.data['results'] if app['reference_number'] == 'APP-001'), None)
        self.assertIsNotNone(app1)
        
        # Check that all required fields are present
        self.assertEqual(app1['reference_number'], 'APP-001')  # Case ID
        self.assertEqual(app1['borrower_name'], 'Jane Doe')  # Borrower Name
        self.assertEqual(app1['stage'], 'inquiry')  # Status code
        self.assertEqual(app1['stage_display'], 'Inquiry')  # Status display
        self.assertEqual(app1['bdm_name'], 'John Manager')  # BDM
        self.assertEqual(app1['guarantor_name'], 'Bob Smith')  # Guarantor Name
        self.assertEqual(app1['purpose'], 'Expanding business operations')  # Case Purpose
        self.assertEqual(app1['product_name'], 'Test Loan Product')  # Product
        self.assertIn('Unit 1 123 Main St Sydney NSW 2000', app1['security_address'])  # Security Address
        self.assertEqual(Decimal(app1['loan_amount']), Decimal('100000'))  # Approved Amount
        self.assertIsNotNone(app1['estimated_settlement_date'])  # Settlement Date
        self.assertIsNotNone(app1['updated_at'])  # Modified Date
        self.assertIsNotNone(app1['created_at'])  # Create Date
        
        # Get the second application from the results
        app2 = next((app for app in response.data['results'] if app['reference_number'] == 'APP-002'), None)
        self.assertIsNotNone(app2)
        
        # Check company borrower name
        self.assertEqual(app2['borrower_name'], 'ABC Company')
        
        # Check legacy security address
        self.assertEqual(app2['security_address'], '456 Security Blvd, Melbourne VIC 3000')
    
    def test_enhanced_applications_endpoint_pagination(self):
        """Test that the enhanced applications endpoint supports pagination"""
        # Create 10 more applications to test pagination
        for i in range(3, 13):
            app = Application.objects.create(
                reference_number=f'APP-{i:03d}',
                loan_amount=Decimal('50000'),
                loan_term=12,
                interest_rate=Decimal('5.0'),
                purpose='Test',
                application_type='residential',
                stage='inquiry',
                created_by=self.user
            )
            app.borrowers.add(self.individual_borrower)
        
        # Request first page with 3 items per page
        response = self.client.get(f'{self.url}?page=1&page_size=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['count'], 12)  # Total of 12 applications
        self.assertIsNotNone(response.data['next'])  # Should have next page
        self.assertIsNone(response.data['previous'])  # No previous page
        
        # Request second page
        response = self.client.get(f'{self.url}?page=2&page_size=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertIsNotNone(response.data['next'])  # Should have next page
        self.assertIsNotNone(response.data['previous'])  # Should have previous page
        
        # Request last page
        response = self.client.get(f'{self.url}?page=4&page_size=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # 3 items on last page
        self.assertIsNone(response.data['next'])  # No next page
        self.assertIsNotNone(response.data['previous'])  # Should have previous page
    
    def test_enhanced_applications_endpoint_filtering(self):
        """Test that the enhanced applications endpoint supports filtering"""
        # Filter by reference_number which is more reliable
        response = self.client.get(f'{self.url}?reference_number=APP-001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'APP-001')
        
        # Filter by application_type
        response = self.client.get(f'{self.url}?application_type=commercial')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Test search functionality
        response = self.client.get(f'{self.url}?search=APP-002')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        found = False
        for app in response.data['results']:
            if app['reference_number'] == 'APP-002':
                found = True
                break
        self.assertTrue(found, "APP-002 should be found in search results")
    
    def test_enhanced_applications_endpoint_unauthorized(self):
        """Test that the enhanced applications endpoint requires authentication"""
        # Use a client without authentication
        client = APIClient()
        response = client.get(self.url)
        
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
