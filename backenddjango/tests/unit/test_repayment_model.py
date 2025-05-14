import pytest
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta

from documents.models import Repayment, Ledger
from applications.models import Application

User = get_user_model()

class RepaymentModelTest(TestCase):
    """Test suite for the Repayment model"""

    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create a test application
        self.application = Application.objects.create(
            reference_number='TEST-APP-001',
            loan_amount=Decimal('100000.00'),
            created_by=self.user
        )

    def test_repayment_creation(self):
        """Test that a repayment can be created"""
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )
        
        self.assertEqual(repayment.amount, Decimal('5000.00'))
        self.assertEqual(repayment.application, self.application)
        self.assertEqual(repayment.created_by, self.user)
        self.assertIsNone(repayment.paid_date)
        self.assertFalse(repayment.reminder_sent)
        self.assertFalse(repayment.overdue_3_day_sent)
        self.assertFalse(repayment.overdue_7_day_sent)
        self.assertFalse(repayment.overdue_10_day_sent)

    def test_repayment_string_representation(self):
        """Test the string representation of a repayment"""
        due_date = timezone.now().date() + timedelta(days=30)
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=due_date,
            application=self.application,
            created_by=self.user
        )
        
        expected_str = f"Repayment $5000.00 due {due_date}"
        self.assertEqual(str(repayment), expected_str)

    def test_repayment_status_change_tracking(self):
        """Test that status changes are properly tracked"""
        # Create a repayment
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )
        
        # Verify initial status flags
        self.assertFalse(repayment.reminder_sent)
        self.assertFalse(repayment.overdue_3_day_sent)
        self.assertFalse(repayment.overdue_7_day_sent)
        self.assertFalse(repayment.overdue_10_day_sent)
        
        # Update status flags
        repayment.reminder_sent = True
        repayment.save()
        
        # Refresh from database
        repayment.refresh_from_db()
        
        # Verify status flag was updated
        self.assertTrue(repayment.reminder_sent)
        self.assertFalse(repayment.overdue_3_day_sent)
        
        # Update multiple status flags
        repayment.overdue_3_day_sent = True
        repayment.overdue_7_day_sent = True
        repayment.save()
        
        # Refresh from database
        repayment.refresh_from_db()
        
        # Verify status flags were updated
        self.assertTrue(repayment.reminder_sent)
        self.assertTrue(repayment.overdue_3_day_sent)
        self.assertTrue(repayment.overdue_7_day_sent)
        self.assertFalse(repayment.overdue_10_day_sent)

    def test_repayment_creates_ledger_entry(self):
        """Test that creating a repayment automatically creates a ledger entry"""
        # Create a repayment
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )
        
        # Check that a ledger entry was created
        ledger_entries = Ledger.objects.filter(
            related_repayment=repayment,
            transaction_type='repayment_scheduled'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, repayment.amount)
        self.assertEqual(ledger_entry.application, self.application)
        self.assertIsNotNone(ledger_entry.transaction_date)

    def test_repayment_payment_creates_ledger_entry(self):
        """Test that marking a repayment as paid creates a ledger entry"""
        # Create a repayment
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )
        
        # Mark the repayment as paid
        payment_date = timezone.now().date()
        repayment.paid_date = payment_date
        repayment.save()
        
        # Check that a ledger entry was created for the payment
        ledger_entries = Ledger.objects.filter(
            related_repayment=repayment,
            transaction_type='repayment_received'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, repayment.amount)
        self.assertEqual(ledger_entry.application, self.application)
        self.assertIsNotNone(ledger_entry.transaction_date)

    def test_repayment_payment_date_change_tracking(self):
        """Test that changes to paid_date are properly tracked"""
        # Create a repayment
        repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )
        
        # Initial ledger entries count (should be 1 for creation)
        initial_ledger_count = Ledger.objects.filter(related_repayment=repayment).count()
        self.assertEqual(initial_ledger_count, 1)
        
        # Set paid_date for the first time
        repayment.paid_date = timezone.now().date()
        repayment.save()
        
        # Should now have 2 ledger entries (creation + payment)
        updated_ledger_count = Ledger.objects.filter(related_repayment=repayment).count()
        self.assertEqual(updated_ledger_count, 2)
        
        # Change paid_date
        repayment.paid_date = timezone.now().date() - timedelta(days=1)
        repayment.save()
        
        # Should still have 2 ledger entries (changing paid_date shouldn't create new entry)
        final_ledger_count = Ledger.objects.filter(related_repayment=repayment).count()
        self.assertEqual(final_ledger_count, 2)

    def test_repayment_ordering(self):
        """Test that repayments are ordered by due_date"""
        # Create multiple repayments with different due dates
        date1 = timezone.now().date() + timedelta(days=10)
        date2 = timezone.now().date() + timedelta(days=20)
        date3 = timezone.now().date() + timedelta(days=30)
        
        repayment3 = Repayment.objects.create(
            amount=Decimal('3000.00'),
            due_date=date3,
            application=self.application,
            created_by=self.user
        )
        
        repayment1 = Repayment.objects.create(
            amount=Decimal('1000.00'),
            due_date=date1,
            application=self.application,
            created_by=self.user
        )
        
        repayment2 = Repayment.objects.create(
            amount=Decimal('2000.00'),
            due_date=date2,
            application=self.application,
            created_by=self.user
        )
        
        # Get all repayments for the application
        repayments = Repayment.objects.filter(application=self.application)
        
        # Check that they are ordered by due_date
        self.assertEqual(repayments[0].due_date, date1)
        self.assertEqual(repayments[1].due_date, date2)
        self.assertEqual(repayments[2].due_date, date3)
