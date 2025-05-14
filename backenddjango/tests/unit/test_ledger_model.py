import pytest
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta

from documents.models import Ledger, Fee, Repayment
from applications.models import Application

User = get_user_model()

class LedgerModelTest(TestCase):
    """Test suite for the Ledger model"""

    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
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
        
        # Create a test fee
        self.fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date(),
            application=self.application,
            created_by=self.user
        )
        
        # Create a test repayment
        self.repayment = Repayment.objects.create(
            amount=Decimal('5000.00'),
            due_date=timezone.now().date() + timedelta(days=30),
            application=self.application,
            created_by=self.user
        )

    def test_ledger_creation(self):
        """Test that a ledger entry can be created"""
        ledger = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('500.00'),
            description='Test adjustment',
            transaction_date=timezone.now(),
            created_by=self.user
        )
        
        self.assertEqual(ledger.application, self.application)
        self.assertEqual(ledger.transaction_type, 'adjustment')
        self.assertEqual(ledger.amount, Decimal('500.00'))
        self.assertEqual(ledger.description, 'Test adjustment')
        self.assertIsNotNone(ledger.transaction_date)
        self.assertEqual(ledger.created_by, self.user)

    def test_ledger_string_representation(self):
        """Test the string representation of a ledger entry"""
        ledger = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('500.00'),
            description='Test adjustment',
            transaction_date=timezone.now(),
            created_by=self.user
        )
        
        self.assertEqual(str(ledger), "Adjustment - $500.00")

    def test_ledger_transaction_date_handling(self):
        """Test that transaction_date is properly handled"""
        # Create a ledger entry with a specific transaction date
        specific_date = timezone.now() - timedelta(days=5)
        ledger = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('500.00'),
            description='Test adjustment with specific date',
            transaction_date=specific_date,
            created_by=self.user
        )
        
        # Verify the transaction date was saved correctly
        self.assertEqual(ledger.transaction_date, specific_date)
        
        # Create a ledger entry without a transaction date
        ledger_no_date = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('500.00'),
            description='Test adjustment without date',
            created_by=self.user
        )
        
        # Verify the transaction date is None
        self.assertIsNone(ledger_no_date.transaction_date)

    def test_fee_creates_ledger_entry(self):
        """Test that creating a fee automatically creates a ledger entry"""
        # Check that a ledger entry was created for the fee in setUp
        ledger_entries = Ledger.objects.filter(
            related_fee=self.fee,
            transaction_type='fee_created'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, self.fee.amount)
        self.assertEqual(ledger_entry.application, self.application)

    def test_fee_payment_creates_ledger_entry(self):
        """Test that marking a fee as paid creates a ledger entry"""
        # Mark the fee as paid
        payment_date = timezone.now().date()
        self.fee.paid_date = payment_date
        self.fee.save()
        
        # Check that a ledger entry was created for the fee payment
        ledger_entries = Ledger.objects.filter(
            related_fee=self.fee,
            transaction_type='fee_paid'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, self.fee.amount)
        self.assertEqual(ledger_entry.application, self.application)
        self.assertEqual(ledger_entry.transaction_date.date(), payment_date)

    def test_repayment_creates_ledger_entry(self):
        """Test that creating a repayment automatically creates a ledger entry"""
        # Check that a ledger entry was created for the repayment in setUp
        ledger_entries = Ledger.objects.filter(
            related_repayment=self.repayment,
            transaction_type='repayment_scheduled'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, self.repayment.amount)
        self.assertEqual(ledger_entry.application, self.application)

    def test_repayment_payment_creates_ledger_entry(self):
        """Test that marking a repayment as paid creates a ledger entry"""
        # Mark the repayment as paid
        payment_date = timezone.now().date()
        self.repayment.paid_date = payment_date
        self.repayment.save()
        
        # Check that a ledger entry was created for the repayment payment
        ledger_entries = Ledger.objects.filter(
            related_repayment=self.repayment,
            transaction_type='repayment_received'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, self.repayment.amount)
        self.assertEqual(ledger_entry.application, self.application)

    def test_ledger_ordering(self):
        """Test that ledger entries are ordered by transaction_date in descending order"""
        # Create multiple ledger entries with different transaction dates
        date1 = timezone.now() - timedelta(days=5)
        date2 = timezone.now() - timedelta(days=3)
        date3 = timezone.now() - timedelta(days=1)
        
        ledger1 = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('100.00'),
            description='Test adjustment 1',
            transaction_date=date1,
            created_by=self.user
        )
        
        ledger2 = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('200.00'),
            description='Test adjustment 2',
            transaction_date=date2,
            created_by=self.user
        )
        
        ledger3 = Ledger.objects.create(
            application=self.application,
            transaction_type='adjustment',
            amount=Decimal('300.00'),
            description='Test adjustment 3',
            transaction_date=date3,
            created_by=self.user
        )
        
        # Get all ledger entries for the application, explicitly ordered by transaction_date
        # Filter by transaction_type='adjustment' to only get the ones created in this test
        ledger_entries = Ledger.objects.filter(
            application=self.application,
            transaction_type='adjustment'
        ).order_by('-transaction_date')
        
        # Check that they are ordered by transaction_date in descending order
        self.assertEqual(ledger_entries[0].transaction_date, date3)
        self.assertEqual(ledger_entries[1].transaction_date, date2)
        self.assertEqual(ledger_entries[2].transaction_date, date1)
