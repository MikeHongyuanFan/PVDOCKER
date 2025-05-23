from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
import json
from datetime import timedelta, date

from applications.models import Application
from documents.models import Repayment  # Import from documents.models, not applications.models
from brokers.models import Broker, BDM
from users.models import User


class RepaymentComplianceUpdateTest(TestCase):
    """
    Test case to verify that the repayment compliance report updates correctly
    when a new repayment is created or updated.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            role='admin'
        )
        
        # Create a test broker
        self.broker = Broker.objects.create(
            name='Test Broker',
            email='broker@example.com',
            phone='1234567890'
        )
        
        # Create a test BDM
        self.bdm = BDM.objects.create(
            name='Test BDM',
            email='bdm@example.com',
            phone='0987654321'
        )
        
        # Create a test application
        self.application = Application.objects.create(
            reference_number='TEST-12345678',
            stage='settled',
            application_type='residential',
            loan_amount=500000.00,
            loan_term=360,
            interest_rate=5.5,
            broker=self.broker,
            bd=self.bdm,
            created_by=self.user
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Define API endpoints
        self.repayment_compliance_url = reverse('repayment-compliance-report')
    
    def test_empty_report_with_no_repayments(self):
        """Test that report shows zeros when no repayments exist."""
        response = self.client.get(self.repayment_compliance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['total_repayments'], 0)
        self.assertEqual(data['paid_on_time'], 0)
        self.assertEqual(data['paid_late'], 0)
        self.assertEqual(data['missed'], 0)
        self.assertEqual(data['compliance_rate'], 0)
    
    def test_report_updates_with_new_repayment(self):
        """Test that report updates when a new repayment is created."""
        # Get initial report
        initial_response = self.client.get(self.repayment_compliance_url)
        initial_data = initial_response.json()
        
        # Create a new repayment directly in the database
        today = timezone.now().date()
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today - timedelta(days=10),
            paid_date=today - timedelta(days=12),  # Paid early (on time)
            created_by=self.user
        )
        
        # Get updated report
        updated_response = self.client.get(self.repayment_compliance_url)
        updated_data = updated_response.json()
        
        # Verify report has been updated
        self.assertEqual(updated_data['total_repayments'], 1)
        self.assertEqual(updated_data['paid_on_time'], 1)
        self.assertEqual(updated_data['paid_late'], 0)
        self.assertEqual(updated_data['missed'], 0)
        self.assertEqual(updated_data['compliance_rate'], 100)
        self.assertEqual(float(updated_data['total_amount_due']), 1500.00)
        self.assertEqual(float(updated_data['total_amount_paid']), 1500.00)
        self.assertEqual(updated_data['payment_rate'], 100)
    
    def test_report_updates_with_late_payment(self):
        """Test that report updates correctly with a late payment."""
        # Create a late payment repayment
        today = timezone.now().date()
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today - timedelta(days=20),
            paid_date=today - timedelta(days=10),  # Paid 10 days late
            created_by=self.user
        )
        
        # Get report
        response = self.client.get(self.repayment_compliance_url)
        data = response.json()
        
        # Verify report metrics
        self.assertEqual(data['total_repayments'], 1)
        self.assertEqual(data['paid_on_time'], 0)
        self.assertEqual(data['paid_late'], 1)
        self.assertEqual(data['missed'], 0)
        self.assertEqual(data['compliance_rate'], 0)
        self.assertEqual(data['average_days_late'], 10)
    
    def test_report_updates_with_missed_payment(self):
        """Test that report updates correctly with a missed payment."""
        # Create a missed payment (due date in past, no paid_date)
        today = timezone.now().date()
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today - timedelta(days=10),
            # No paid_date means it's missed
            created_by=self.user
        )
        
        # Get report
        response = self.client.get(self.repayment_compliance_url)
        data = response.json()
        
        # Verify report metrics
        self.assertEqual(data['total_repayments'], 1)
        self.assertEqual(data['paid_on_time'], 0)
        self.assertEqual(data['paid_late'], 0)
        self.assertEqual(data['missed'], 1)
        self.assertEqual(data['compliance_rate'], 0)
    
    def test_report_updates_with_scheduled_future_payment(self):
        """Test that report correctly handles scheduled future payments."""
        # Create a scheduled payment that is in the future
        today = timezone.now().date()
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today + timedelta(days=5),  # Due date in the future
            # No paid_date means it's scheduled
            created_by=self.user
        )
        
        # Get report
        response = self.client.get(self.repayment_compliance_url)
        data = response.json()
        
        # Verify report metrics - should count in total but not as missed
        self.assertEqual(data['total_repayments'], 1)
        self.assertEqual(data['paid_on_time'], 0)
        self.assertEqual(data['paid_late'], 0)
        self.assertEqual(data['missed'], 0)  # Not missed because due date is in future
        self.assertEqual(data['compliance_rate'], 0)
    
    def test_report_with_multiple_repayments(self):
        """Test report with a mix of on-time, late, and missed payments."""
        today = timezone.now().date()
        
        # Create multiple repayments with different statuses
        repayments = [
            # On-time payment
            Repayment.objects.create(
                application=self.application,
                amount=1500.00,
                due_date=today - timedelta(days=30),
                paid_date=today - timedelta(days=30),
                created_by=self.user
            ),
            # Late payment
            Repayment.objects.create(
                application=self.application,
                amount=1500.00,
                due_date=today - timedelta(days=20),
                paid_date=today - timedelta(days=15),
                created_by=self.user
            ),
            # Missed payment
            Repayment.objects.create(
                application=self.application,
                amount=1500.00,
                due_date=today - timedelta(days=10),
                # No paid_date means it's missed
                created_by=self.user
            ),
            # Future scheduled payment (should not count as missed)
            Repayment.objects.create(
                application=self.application,
                amount=1500.00,
                due_date=today + timedelta(days=10),
                # No paid_date means it's scheduled
                created_by=self.user
            )
        ]
        
        # Get report
        response = self.client.get(self.repayment_compliance_url)
        data = response.json()
        
        # Verify report metrics
        self.assertEqual(data['total_repayments'], 4)
        self.assertEqual(data['paid_on_time'], 1)
        self.assertEqual(data['paid_late'], 1)
        self.assertEqual(data['missed'], 1)  # Only counts past due dates
        self.assertEqual(data['compliance_rate'], 25)  # 1/4 = 25%
        self.assertEqual(float(data['total_amount_due']), 6000.00)
        self.assertEqual(float(data['total_amount_paid']), 3000.00)
        self.assertEqual(data['payment_rate'], 50)  # 3000/6000 = 50%
    
    def test_report_with_null_paid_date(self):
        """Test that report handles repayments with null paid_date correctly."""
        today = timezone.now().date()
        
        # Create a repayment with null paid_date
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today - timedelta(days=5),
            # No paid_date
            created_by=self.user
        )
        
        # Get report
        response = self.client.get(self.repayment_compliance_url)
        data = response.json()
        
        # Verify report metrics - should handle null paid_date gracefully
        self.assertEqual(data['total_repayments'], 1)
        # Since paid_date is null and due_date is in the past, it should count as missed
        self.assertEqual(data['paid_on_time'], 0)
        self.assertEqual(data['paid_late'], 0)
        self.assertEqual(data['missed'], 1)
    
    def test_fix_for_null_paid_date_issue(self):
        """Test the fixed implementation for handling null paid_date values."""
        # Create test data
        today = timezone.now().date()
        repayment = Repayment.objects.create(
            application=self.application,
            amount=1500.00,
            due_date=today - timedelta(days=5),
            # No paid_date initially
            created_by=self.user
        )
        
        # Get initial report
        initial_response = self.client.get(self.repayment_compliance_url)
        initial_data = initial_response.json()
        
        # Verify it's counted as missed
        self.assertEqual(initial_data['missed'], 1)
        
        # Now update with a paid_date
        repayment.paid_date = today - timedelta(days=6)  # Paid before due date
        repayment.save()
        
        # Get updated report
        updated_response = self.client.get(self.repayment_compliance_url)
        updated_data = updated_response.json()
        
        # Now it should count as paid on time
        self.assertEqual(updated_data['paid_on_time'], 1)
        self.assertEqual(updated_data['missed'], 0)


if __name__ == '__main__':
    import unittest
    unittest.main()
