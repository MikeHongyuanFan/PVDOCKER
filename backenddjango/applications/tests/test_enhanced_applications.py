from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Application
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

class EnhancedApplicationsFilterTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test applications with different attributes
        self.app1 = Application.objects.create(
            reference_number='REF001',
            loan_amount=Decimal('100000.00'),
            purpose='Business Expansion',
            stage='inquiry',
            estimated_settlement_date=datetime.now().date()
        )
        
        self.app2 = Application.objects.create(
            reference_number='REF002',
            loan_amount=Decimal('200000.00'),
            purpose='Property Purchase',
            stage='approved',
            estimated_settlement_date=(datetime.now() + timedelta(days=30)).date()
        )
        
        self.app3 = Application.objects.create(
            reference_number='REF003',
            loan_amount=Decimal('300000.00'),
            purpose='Refinance',
            stage='settled',
            estimated_settlement_date=(datetime.now() - timedelta(days=30)).date()
        )
        
        self.url = reverse('enhanced-application-list')

    def test_filter_by_reference_number(self):
        response = self.client.get(f'{self.url}?reference_number=REF001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF001')

    def test_filter_by_loan_amount_range(self):
        response = self.client.get(f'{self.url}?min_loan_amount=150000&max_loan_amount=250000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF002')

    def test_filter_by_stage(self):
        response = self.client.get(f'{self.url}?stage=approved')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF002')

    def test_filter_by_purpose(self):
        response = self.client.get(f'{self.url}?search=Refinance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF003')

    def test_filter_by_date_range(self):
        today = datetime.now().date()
        future_date = (today + timedelta(days=60)).strftime('%Y-%m-%d')
        past_date = (today - timedelta(days=60)).strftime('%Y-%m-%d')
        
        response = self.client.get(
            f'{self.url}?estimated_settlement_date_after={past_date}&estimated_settlement_date_before={future_date}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Should return all applications

    def test_search_filter(self):
        response = self.client.get(f'{self.url}?search=Business')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF001')

    def test_multiple_filters(self):
        response = self.client.get(
            f'{self.url}?min_loan_amount=200000&stage=approved'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF002')

    def test_invalid_filter_values(self):
        response = self.client.get(f'{self.url}?min_loan_amount=invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination(self):
        response = self.client.get(f'{self.url}?page_size=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNotNone(response.data['next'])
        
    def test_metadata_in_response(self):
        response = self.client.get(f'{self.url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('metadata', response.data)
        self.assertIn('filter_options', response.data['metadata'])
        self.assertIn('stages', response.data['metadata']['filter_options'])
        self.assertIn('application_types', response.data['metadata']['filter_options'])
        
    def test_sorting(self):
        # Test ascending sort by loan_amount
        response = self.client.get(f'{self.url}?sort_by=loan_amount&sort_direction=asc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF001')
        self.assertEqual(response.data['results'][2]['reference_number'], 'REF003')
        
        # Test descending sort by loan_amount
        response = self.client.get(f'{self.url}?sort_by=loan_amount&sort_direction=desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['reference_number'], 'REF003')
        self.assertEqual(response.data['results'][2]['reference_number'], 'REF001')
