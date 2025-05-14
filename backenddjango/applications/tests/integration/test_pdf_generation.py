import os
import tempfile
from decimal import Decimal
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from applications.models import Application, SecurityProperty, LoanRequirement
from borrowers.models import Borrower
from brokers.models import Broker, BDM, Branch
from applications.utils.pdf_filler import fill_pdf_form, extract_application_data
from pdfrw import PdfReader

User = get_user_model()

# Create a temporary media directory for test files
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PDFGenerationIntegrationTest(TestCase):
    """Integration tests for PDF generation functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create a test user with admin privileges
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            is_staff=True,
            is_superuser=True
        )
        self.admin_user.role = 'admin'
        self.admin_user.save()
        
        # Create a broker user with proper role and broker association
        self.broker_user = User.objects.create_user(
            username='broker',
            email='broker@example.com',
            password='password123'
        )
        self.broker_user.role = 'broker'
        self.broker_user.save()
        
        # Create a broker entity and associate with the broker user
        self.broker = Broker.objects.create(
            user=self.broker_user,
            name="Test Broker",
            email="broker@example.com",
            phone="0412345678",
            created_by=self.admin_user
        )
        
        # Create a BDM user
        self.bdm_user = User.objects.create_user(
            username='bdm',
            email='bdm@example.com',
            password='password123'
        )
        self.bdm_user.role = 'bd'
        self.bdm_user.save()
        
        # Create a BDM entity and associate with the BDM user
        self.bdm = BDM.objects.create(
            user=self.bdm_user,
            name="Test BDM",
            email="bdm@example.com",
            phone="0412345679",
            created_by=self.admin_user
        )
        
        # Create a branch
        self.branch = Branch.objects.create(
            name="Test Branch",
            address="123 Branch St",
            created_by=self.admin_user
        )
        
        # Create a test application with all required fields
        self.application = Application.objects.create(
            reference_number='TEST-2025-001',
            loan_amount=Decimal('500000.00'),
            loan_term=24,
            interest_rate=Decimal('5.75'),
            loan_purpose='purchase',
            exit_strategy='refinance',
            additional_comments='Test application for PDF generation',
            repayment_frequency='monthly',
            security_address='123 Test Street, Sydney NSW 2000',
            security_type='residential',
            security_value=Decimal('750000.00'),
            created_by=self.admin_user,
            broker=self.broker,  # Associate with broker
            bd=self.bdm,         # Associate with BDM
            branch=self.branch   # Associate with branch
        )
        
        # Create an individual borrower
        self.individual_borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='0412345678',
            residential_address='456 Borrower Street, Melbourne VIC 3000',
            annual_income=Decimal('120000.00'),
            is_company=False,
            created_by=self.admin_user
        )
        self.application.borrowers.add(self.individual_borrower)
        
        # Create a company borrower
        self.company_borrower = Borrower.objects.create(
            company_name='Test Company Pty Ltd',
            company_abn='12345678901',
            company_acn='123456789',
            registered_address_street_no='789',
            registered_address_street_name='Company Road',
            registered_address_suburb='Brisbane',
            registered_address_state='QLD',
            registered_address_postcode='4000',
            annual_company_income=Decimal('500000.00'),
            is_company=True,
            created_by=self.admin_user
        )
        self.application.borrowers.add(self.company_borrower)
        
        # Create a security property
        self.security_property = SecurityProperty.objects.create(
            application=self.application,
            address_street_no='123',
            address_street_name='Test Street',
            address_suburb='Sydney',
            address_state='NSW',
            address_postcode='2000',
            property_type='residential',
            estimated_value=Decimal('750000.00')
        )
        
        # Create a loan requirement
        self.loan_requirement = LoanRequirement.objects.create(
            application=self.application,
            description='Property purchase',
            amount=Decimal('500000.00')
        )
        
        # Set up API client
        self.client = APIClient()
        
    def test_extract_application_data(self):
        """Test that application data is correctly extracted"""
        data = extract_application_data(self.application)
        
        # Check application fields
        self.assertEqual(data['reference_number'], 'TEST-2025-001')
        self.assertEqual(data['loan_amount'], Decimal('500000.00'))
        self.assertEqual(data['loan_term'], 24)
        self.assertEqual(data['interest_rate'], Decimal('5.75'))
        self.assertEqual(data['loan_purpose'], 'Purchase')  # Display value
        self.assertEqual(data['exit_strategy'], 'Refinance')  # Display value
        self.assertEqual(data['additional_comments'], 'Test application for PDF generation')
        self.assertEqual(data['repayment_frequency'], 'Monthly')  # Display value
        
        # Check individual borrower fields
        self.assertEqual(data['borrower_first_name'], 'John')
        self.assertEqual(data['borrower_last_name'], 'Doe')
        self.assertEqual(data['borrower_email'], 'john.doe@example.com')
        self.assertEqual(data['borrower_phone'], '0412345678')
        self.assertEqual(data['borrower_residential_address'], '456 Borrower Street, Melbourne VIC 3000')
        self.assertEqual(data['borrower_annual_income'], Decimal('120000.00'))
        
        # Check company borrower fields
        self.assertEqual(data['company_name'], 'Test Company Pty Ltd')
        self.assertEqual(data['company_abn'], '12345678901')
        self.assertEqual(data['company_acn'], '123456789')
        self.assertEqual(data['company_address'], '789 Company Road Brisbane QLD 4000')
        self.assertEqual(data['annual_company_income'], Decimal('500000.00'))
        
        # Check loan requirement fields
        self.assertEqual(data['loan_requirement_description'], 'Property purchase')
        self.assertEqual(data['loan_requirement_amount'], Decimal('500000.00'))
        
        # Check security property fields
        self.assertEqual(data['security_address'], '123 Test Street Sydney NSW 2000')
        self.assertEqual(data['security_type'], 'Residential')  # Display value
        self.assertEqual(data['security_value'], Decimal('750000.00'))
    
    def test_fill_pdf_form(self):
        """Test that PDF form is filled correctly"""
        # Create a temporary output file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_path = temp_file.name
        
        try:
            # Fill the PDF form
            missing_fields = fill_pdf_form(self.application, output_path)
            
            # Check that the PDF file was created
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that there are no missing fields
            self.assertEqual(len(missing_fields), 0)
            
            # Verify PDF content (basic check that it's a valid PDF)
            pdf = PdfReader(output_path)
            self.assertIsNotNone(pdf)
            self.assertTrue(len(pdf.pages) > 0)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_generate_pdf_api_endpoint_get(self):
        """Test the GET API endpoint for generating a PDF"""
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make a GET request to the PDF generation endpoint
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.get(url)
        
        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response is a PDF file
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])
        self.assertTrue(f'{self.application.reference_number}' in response['Content-Disposition'])
    
    def test_generate_pdf_api_endpoint_post(self):
        """Test the POST API endpoint for generating a PDF"""
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make a POST request to the PDF generation endpoint
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.post(url)
        
        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected data
        self.assertIn('pdf_path', response.data)
        self.assertIn('missing_fields', response.data)
        self.assertEqual(len(response.data['missing_fields']), 0)
        
        # Check that the PDF file was created
        pdf_path = os.path.join(TEMP_MEDIA_ROOT, response.data['pdf_path'].replace('media/', ''))
        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(os.path.getsize(pdf_path) > 0)
    
    def test_generate_pdf_with_missing_fields(self):
        """Test PDF generation with missing fields"""
        # Create an application with minimal data
        minimal_application = Application.objects.create(
            reference_number='TEST-2025-002',
            loan_amount=Decimal('300000.00'),
            created_by=self.admin_user
        )
        
        # Create a temporary output file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_path = temp_file.name
        
        try:
            # Fill the PDF form
            missing_fields = fill_pdf_form(minimal_application, output_path)
            
            # Check that the PDF file was created
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(os.path.getsize(output_path) > 0)
            
            # Check that there are missing fields
            self.assertTrue(len(missing_fields) > 0)
            
            # Verify some expected missing fields
            expected_missing = ['loan_term', 'interest_rate', 'loan_purpose']
            for field in expected_missing:
                self.assertIn(field, missing_fields)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_permission_checks(self):
        """Test permission checks for PDF generation"""
        # Create a regular user with no special permissions
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='password123'
        )
        
        # Test with regular user (should be denied)
        self.client.force_authenticate(user=regular_user)
        url = reverse('application-generate-pdf', args=[self.application.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with broker user (should be allowed)
        self.client.force_authenticate(user=self.broker_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with admin user (should be allowed)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_nonexistent_application(self):
        """Test PDF generation with a non-existent application ID"""
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make a request with a non-existent application ID
        url = reverse('application-generate-pdf', args=[99999])
        response = self.client.get(url)
        
        # Check that the response is a 404 error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertIn('not found', response.data['error'])
    
    def test_strict_mode(self):
        """Test PDF generation with strict mode enabled"""
        # Create an application with minimal data
        minimal_application = Application.objects.create(
            reference_number='TEST-2025-003',
            loan_amount=Decimal('300000.00'),
            created_by=self.admin_user
        )
        
        # Login as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Make a POST request with strict mode enabled
        url = reverse('application-generate-pdf', args=[minimal_application.id])
        response = self.client.post(f"{url}?strict=true")
        
        # Check that the response is a 400 error due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('missing_fields', response.data)
        self.assertTrue(len(response.data['missing_fields']) > 0)
