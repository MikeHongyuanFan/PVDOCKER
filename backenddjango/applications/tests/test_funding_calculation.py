from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from applications.models import Application, FundingCalculationHistory
from decimal import Decimal

User = get_user_model()


class FundingCalculationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='admin'
        )
        
        # Create a test application
        self.application = Application.objects.create(
            loan_amount=Decimal('1000000.00'),
            loan_term=24,
            interest_rate=Decimal('5.5'),
            security_value=Decimal('1500000.00'),
            created_by=self.user
        )
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Define the funding calculation input
        self.funding_input = {
            'establishment_fee_rate': '2.5',
            'capped_interest_months': 9,
            'monthly_line_fee_rate': '1.2',
            'brokerage_fee_rate': '1.0',
            'application_fee': '1000.00',
            'due_diligence_fee': '2500.00',
            'legal_fee_before_gst': '3000.00',
            'valuation_fee': '1500.00',
            'monthly_account_fee': '100.00',
            'working_fee': '500.00'
        }
    
    def test_create_funding_calculation(self):
        """Test creating a funding calculation for an application"""
        url = reverse('application-funding-calculation', args=[self.application.id])
        response = self.client.post(url, self.funding_input, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the calculation result is returned
        self.assertIn('calculation_result', response.data)
        self.assertIn('total_fees', response.data['calculation_result'])
        self.assertIn('funds_available', response.data['calculation_result'])
        
        # Check that the application was updated with the funding result
        self.application.refresh_from_db()
        self.assertIsNotNone(self.application.funding_result)
        
        # Check that a funding calculation history record was created
        history_count = FundingCalculationHistory.objects.filter(application=self.application).count()
        self.assertEqual(history_count, 1)
    
    def test_get_funding_calculation_history(self):
        """Test retrieving funding calculation history for an application"""
        # First create a calculation
        url = reverse('application-funding-calculation', args=[self.application.id])
        self.client.post(url, self.funding_input, format='json')
        
        # Then get the history
        url = reverse('application-funding-calculation-history', args=[self.application.id])
        response = self.client.get(url)
        
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the history is returned
        self.assertEqual(len(response.data), 1)
        self.assertIn('calculation_input', response.data[0])
        self.assertIn('calculation_result', response.data[0])
    
    def test_create_application_with_funding_calculation(self):
        """Test creating an application with funding calculation"""
        url = reverse('application-list')
        
        data = {
            'loan_amount': '2000000.00',
            'loan_term': 36,
            'interest_rate': '6.0',
            'security_value': '3000000.00',
            'application_type': 'commercial',
            'purpose': 'Test purpose',
            'funding_calculation_input': self.funding_input
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the created application
        application_id = response.data['id']
        application = Application.objects.get(id=application_id)
        
        # Check that the funding result was calculated
        self.assertIsNotNone(application.funding_result)
        
        # Check that a funding calculation history record was created
        history_count = FundingCalculationHistory.objects.filter(application=application).count()
        self.assertEqual(history_count, 1)