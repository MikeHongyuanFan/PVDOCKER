from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from users.models import User
from applications.models import Application, Repayment


class RepaymentComplianceReportTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            role='admin'
        )
        self.client.force_authenticate(user=self.user)

        # Create test application
        self.application = Application.objects.create(
            loan_amount=100000,
            loan_term=12,
            interest_rate=5.0,
            purpose='Test Application'
        )

        # Set up dates for testing
        self.today = timezone.now().date()
        self.yesterday = self.today - timedelta(days=1)
        self.last_week = self.today - timedelta(days=7)
        self.next_week = self.today + timedelta(days=7)

    def create_repayment(self, **kwargs):
        """Helper method to create a repayment with default values"""
        defaults = {
            'application': self.application,
            'amount': Decimal('1000.00'),
            'due_date': self.today,
            'status': 'scheduled'
        }
        defaults.update(kwargs)
        return Repayment.objects.create(**defaults)

    def test_repayment_compliance_basic(self):
        """Test basic repayment compliance report with no repayments"""
        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_repayments'], 0)
        self.assertEqual(response.data['paid_on_time'], 0)
        self.assertEqual(response.data['missed'], 0)

    def test_paid_on_time_repayments(self):
        """Test repayments that were paid on time"""
        # Create a repayment paid on time
        self.create_repayment(
            due_date=self.yesterday,
            paid_date=self.yesterday,
            status='paid',
            payment_amount=Decimal('1000.00')
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_repayments'], 1)
        self.assertEqual(response.data['paid_on_time'], 1)
        self.assertEqual(response.data['paid_late'], 0)
        self.assertEqual(response.data['compliance_rate'], 100.0)

    def test_paid_late_repayments(self):
        """Test repayments that were paid late"""
        # Create a repayment paid late
        self.create_repayment(
            due_date=self.last_week,
            paid_date=self.yesterday,
            status='paid',
            payment_amount=Decimal('1000.00')
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['paid_late'], 1)
        self.assertTrue(response.data['average_days_late'] > 0)

    def test_partial_payments(self):
        """Test partial payment handling"""
        # Create a partial payment
        self.create_repayment(
            due_date=self.yesterday,
            paid_date=self.yesterday,
            status='partial',
            amount=Decimal('1000.00'),
            payment_amount=Decimal('500.00')
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_amount_due']), Decimal('1000.00'))
        self.assertEqual(Decimal(response.data['total_amount_paid']), Decimal('500.00'))
        self.assertEqual(response.data['payment_rate'], 50.0)

    def test_missed_repayments(self):
        """Test missed repayments handling"""
        # Create a missed repayment
        self.create_repayment(
            due_date=self.last_week,
            status='missed'
        )
        # Create an overdue scheduled repayment
        self.create_repayment(
            due_date=self.last_week,
            status='scheduled'
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['missed'], 2)  # Both should be counted as missed

    def test_monthly_breakdown(self):
        """Test monthly breakdown calculations"""
        # Create repayments across different months
        last_month = self.today.replace(day=1) - timedelta(days=1)
        
        # Last month - paid on time
        self.create_repayment(
            due_date=last_month,
            paid_date=last_month,
            status='paid',
            payment_amount=Decimal('1000.00')
        )
        
        # This month - paid late
        self.create_repayment(
            due_date=self.last_week,
            paid_date=self.today,
            status='paid',
            payment_amount=Decimal('1000.00')
        )
        
        # This month - partial payment
        self.create_repayment(
            due_date=self.yesterday,
            paid_date=self.yesterday,
            status='partial',
            amount=Decimal('1000.00'),
            payment_amount=Decimal('500.00')
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify monthly breakdown exists and has correct structure
        self.assertTrue('monthly_breakdown' in response.data)
        self.assertTrue(len(response.data['monthly_breakdown']) >= 2)  # At least 2 months
        
        # Find current month's data
        current_month = next(
            (m for m in response.data['monthly_breakdown'] 
             if m['month'] == self.today.strftime('%Y-%m')),
            None
        )
        
        self.assertIsNotNone(current_month)
        self.assertTrue(current_month)
        self.assertEqual(current_month['total_repayments'], 2)
        self.assertEqual(current_month['paid_on_time'], 1)  # The partial payment
        self.assertEqual(current_month['paid_late'], 1)  # The late payment

    def test_date_filtering(self):
        """Test date range filtering"""
        # Create repayments across different dates
        self.create_repayment(
            due_date=self.last_week,
            paid_date=self.last_week,
            status='paid'
        )
        self.create_repayment(
            due_date=self.next_week,
            status='scheduled'
        )

        url = reverse('repayment-compliance-report')
        response = self.client.get(f"{url}?start_date={self.today}&end_date={self.next_week}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_repayments'], 1)  # Only the future repayment

    def test_application_filtering(self):
        """Test filtering by application ID"""
        # Create another application and repayment
        other_application = Application.objects.create(
            loan_amount=200000,
            loan_term=24,
            interest_rate=6.0,
            purpose='Other Test Application'
        )
        self.create_repayment(application=other_application)
        self.create_repayment(application=self.application)

        url = reverse('repayment-compliance-report')
        response = self.client.get(f"{url}?application_id={self.application.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_repayments'], 1)  # Only repayments for the specified application
