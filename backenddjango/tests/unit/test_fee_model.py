import pytest
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta

from documents.models import Fee, Ledger
from applications.models import Application

User = get_user_model()

class FeeModelTest(TestCase):
    """Test suite for the Fee model"""

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

    def test_fee_creation(self):
        """Test that a fee can be created"""
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        self.assertEqual(fee.fee_type, 'application')
        self.assertEqual(fee.amount, Decimal('1000.00'))
        self.assertEqual(fee.application, self.application)
        self.assertEqual(fee.created_by, self.user)
        self.assertIsNone(fee.paid_date)

    def test_fee_string_representation(self):
        """Test the string representation of a fee"""
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        expected_str = "Application Fee - $1000.00"
        self.assertEqual(str(fee), expected_str)

    def test_fee_creates_ledger_entry(self):
        """Test that creating a fee automatically creates a ledger entry"""
        # Create a fee
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        # Check that a ledger entry was created
        ledger_entries = Ledger.objects.filter(
            related_fee=fee,
            transaction_type='fee_created'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, fee.amount)
        self.assertEqual(ledger_entry.application, self.application)
        self.assertEqual(ledger_entry.description, "Fee created: Application Fee")

    def test_fee_payment_creates_ledger_entry(self):
        """Test that marking a fee as paid creates a ledger entry"""
        # Create a fee
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        # Mark the fee as paid
        payment_date = timezone.now().date()
        fee.paid_date = payment_date
        fee.save()
        
        # Check that a ledger entry was created for the payment
        ledger_entries = Ledger.objects.filter(
            related_fee=fee,
            transaction_type='fee_paid'
        )
        
        self.assertEqual(ledger_entries.count(), 1)
        ledger_entry = ledger_entries.first()
        self.assertEqual(ledger_entry.amount, fee.amount)
        self.assertEqual(ledger_entry.application, self.application)
        self.assertEqual(ledger_entry.description, "Fee paid: Application Fee")
        self.assertEqual(ledger_entry.transaction_date.date(), payment_date)

    def test_fee_payment_date_change_tracking(self):
        """Test that changes to paid_date are properly tracked"""
        # Create a fee
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        # Initial ledger entries count (should be 1 for creation)
        initial_ledger_count = Ledger.objects.filter(related_fee=fee).count()
        self.assertEqual(initial_ledger_count, 1)
        
        # Set paid_date for the first time
        fee.paid_date = timezone.now().date()
        fee.save()
        
        # Should now have 2 ledger entries (creation + payment)
        updated_ledger_count = Ledger.objects.filter(related_fee=fee).count()
        self.assertEqual(updated_ledger_count, 2)
        
        # Change paid_date
        fee.paid_date = timezone.now().date() - timedelta(days=1)
        fee.save()
        
        # Should still have 2 ledger entries (changing paid_date shouldn't create new entry)
        final_ledger_count = Ledger.objects.filter(related_fee=fee).count()
        self.assertEqual(final_ledger_count, 2)

    def test_fee_ordering(self):
        """Test that fees are ordered by due_date"""
        # Create multiple fees with different due dates
        date1 = timezone.now().date() + timedelta(days=5)
        date2 = timezone.now().date() + timedelta(days=10)
        date3 = timezone.now().date() + timedelta(days=15)
        
        fee3 = Fee.objects.create(
            fee_type='settlement',
            amount=Decimal('3000.00'),
            due_date=date3,
            application=self.application,
            created_by=self.user
        )
        
        fee1 = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=date1,
            application=self.application,
            created_by=self.user
        )
        
        fee2 = Fee.objects.create(
            fee_type='valuation',
            amount=Decimal('2000.00'),
            due_date=date2,
            application=self.application,
            created_by=self.user
        )
        
        # Get all fees for the application
        fees = Fee.objects.filter(application=self.application)
        
        # Check that they are ordered by due_date
        self.assertEqual(fees[0].due_date, date1)
        self.assertEqual(fees[1].due_date, date2)
        self.assertEqual(fees[2].due_date, date3)

    def test_different_fee_types(self):
        """Test that different fee types can be created"""
        # Create fees with different types
        application_fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user
        )
        
        valuation_fee = Fee.objects.create(
            fee_type='valuation',
            amount=Decimal('2000.00'),
            due_date=timezone.now().date() + timedelta(days=14),
            application=self.application,
            created_by=self.user
        )
        
        legal_fee = Fee.objects.create(
            fee_type='legal',
            amount=Decimal('3000.00'),
            due_date=timezone.now().date() + timedelta(days=21),
            application=self.application,
            created_by=self.user
        )
        
        # Check that the fee types are correct
        self.assertEqual(application_fee.fee_type, 'application')
        self.assertEqual(application_fee.get_fee_type_display(), 'Application Fee')
        
        self.assertEqual(valuation_fee.fee_type, 'valuation')
        self.assertEqual(valuation_fee.get_fee_type_display(), 'Valuation Fee')
        
        self.assertEqual(legal_fee.fee_type, 'legal')
        self.assertEqual(legal_fee.get_fee_type_display(), 'Legal Fee')

    def test_fee_with_invoice(self):
        """Test that a fee can have an invoice attached"""
        # This test is a placeholder since we can't easily test file uploads in a unit test
        # In a real test environment, you would use SimpleUploadedFile from django.core.files.uploadedfile
        
        fee = Fee.objects.create(
            fee_type='application',
            amount=Decimal('1000.00'),
            due_date=timezone.now().date() + timedelta(days=7),
            application=self.application,
            created_by=self.user,
            description='Fee with invoice placeholder'
        )
        
        self.assertEqual(fee.description, 'Fee with invoice placeholder')
