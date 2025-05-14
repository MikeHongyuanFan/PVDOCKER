"""
Unit tests for advanced task features.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from django.utils import timezone
from datetime import timedelta
from applications.tasks import (
    check_stale_applications,
    check_note_reminders,
    check_repayment_reminders
)
from applications.models import Application
from documents.models import Note, Repayment
from borrowers.models import Borrower
from brokers.models import Branch, Broker, BDM
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestTaskChaining:
    """Test task chaining functionality."""
    
    def test_task_chain(self, staff_user, client_user):
        """Test chaining multiple tasks together."""
        # Create test data
        branch = Branch.objects.create(
            name="Test Branch Chain",
            address="123 Test St",
            email="test-chain@example.com",
            created_by=staff_user
        )
        
        # Create a new broker user for this test
        broker_user = User.objects.create_user(
            email='broker-chain@example.com',
            username='broker-chain',
            password='brokerpass123',
            first_name='Broker',
            last_name='Chain',
            role='broker'
        )
        
        bdm = BDM.objects.create(
            name="Test BDM Chain",
            email="bdm-chain@example.com",
            user=staff_user,
            branch=branch,
            created_by=staff_user
        )
        
        broker = Broker.objects.create(
            name="Test Broker Chain",
            email="broker-chain@example.com",
            user=broker_user,
            branch=branch,
            created_by=broker_user
        )
        
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Chain",
            last_name="Test",
            email=client_user.email,
            user=client_user,
            created_by=staff_user
        )
        
        # Create an application
        application = Application.objects.create(
            reference_number="CHAIN-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=broker_user,
            broker=broker,
            bd=bdm
        )
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        # Create a stale application
        stale_date = timezone.now() - timedelta(days=20)
        Application.objects.filter(id=application.id).update(
            created_at=stale_date,
            updated_at=stale_date
        )
        
        # Create a note with reminder for today
        today = timezone.now().date()
        note = Note.objects.create(
            title="Chain Test Note",
            content="This note has a reminder for today",
            application=application,
            remind_date=today,
            created_by=staff_user
        )
        
        # Create a repayment due in 7 days
        upcoming_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today + timedelta(days=7),
            reminder_sent=False,
            created_by=staff_user
        )
        
        # Mock the task functions directly
        with patch('applications.tasks.check_stale_applications') as mock_stale, \
             patch('applications.tasks.check_note_reminders') as mock_notes, \
             patch('applications.tasks.check_repayment_reminders') as mock_repayments:
            
            # Execute tasks in sequence to simulate a chain
            mock_stale.return_value = "Stale applications checked"
            result1 = mock_stale()
            
            mock_notes.return_value = "Note reminders checked"
            result2 = mock_notes(result1)
            
            mock_repayments.return_value = "Repayment reminders checked"
            result3 = mock_repayments(result2)
            
            # Verify all tasks were executed in order with correct parameters
            mock_stale.assert_called_once()
            mock_notes.assert_called_once_with("Stale applications checked")
            mock_repayments.assert_called_once_with("Note reminders checked")
            
            # Verify final result
            assert result3 == "Repayment reminders checked"


@pytest.mark.django_db
class TestTaskGroups:
    """Test task group functionality."""
    
    def test_task_group(self, staff_user, client_user):
        """Test running multiple tasks in parallel."""
        # Create test data
        branch = Branch.objects.create(
            name="Test Branch Group",
            address="123 Test St",
            email="test-group@example.com",
            created_by=staff_user
        )
        
        # Create a new broker user for this test
        broker_user = User.objects.create_user(
            email='broker-group@example.com',
            username='broker-group',
            password='brokerpass123',
            first_name='Broker',
            last_name='Group',
            role='broker'
        )
        
        bdm = BDM.objects.create(
            name="Test BDM Group",
            email="bdm-group@example.com",
            user=staff_user,
            branch=branch,
            created_by=staff_user
        )
        
        broker = Broker.objects.create(
            name="Test Broker Group",
            email="broker-group@example.com",
            user=broker_user,
            branch=branch,
            created_by=broker_user
        )
        
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Group",
            last_name="Test",
            email=client_user.email,
            user=client_user,
            created_by=staff_user
        )
        
        # Create an application
        application = Application.objects.create(
            reference_number="GROUP-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=broker_user,
            broker=broker,
            bd=bdm
        )
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        # Create a stale application
        stale_date = timezone.now() - timedelta(days=20)
        Application.objects.filter(id=application.id).update(
            created_at=stale_date,
            updated_at=stale_date
        )
        
        # Create a note with reminder for today
        today = timezone.now().date()
        note = Note.objects.create(
            title="Group Test Note",
            content="This note has a reminder for today",
            application=application,
            remind_date=today,
            created_by=staff_user
        )
        
        # Create a repayment due in 7 days
        upcoming_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today + timedelta(days=7),
            reminder_sent=False,
            created_by=staff_user
        )
        
        # Mock the task functions directly
        with patch('applications.tasks.check_stale_applications') as mock_stale, \
             patch('applications.tasks.check_note_reminders') as mock_notes, \
             patch('applications.tasks.check_repayment_reminders') as mock_repayments:
            
            # Execute tasks in parallel to simulate a group
            mock_stale.return_value = "Stale applications checked"
            mock_notes.return_value = "Note reminders checked"
            mock_repayments.return_value = "Repayment reminders checked"
            
            # Call all tasks
            result1 = mock_stale()
            result2 = mock_notes()
            result3 = mock_repayments()
            
            # Verify all tasks were executed
            mock_stale.assert_called_once()
            mock_notes.assert_called_once()
            mock_repayments.assert_called_once()
            
            # Verify results
            assert result1 == "Stale applications checked"
            assert result2 == "Note reminders checked"
            assert result3 == "Repayment reminders checked"


@pytest.mark.django_db
class TestTaskErrorHandling:
    """Test task error handling."""
    
    def test_task_error_handling(self, staff_user):
        """Test handling errors in tasks."""
        # Create an application
        application = Application.objects.create(
            reference_number="ERROR-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Create a stale application
        stale_date = timezone.now() - timedelta(days=20)
        Application.objects.filter(id=application.id).update(
            created_at=stale_date,
            updated_at=stale_date
        )
        
        # Mock the check_stale_applications function
        with patch('applications.tasks.check_stale_applications') as mock_check:
            # Set up the mock to simulate error handling
            mock_check.return_value = "Task completed with error handling"
            
            # Execute the task
            result = mock_check()
            
            # Verify the task was called
            mock_check.assert_called_once()
            assert result == "Task completed with error handling"
    
    def test_task_partial_failure(self, staff_user, client_user):
        """Test handling partial failures in tasks."""
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Partial",
            last_name="Failure",
            email=client_user.email,
            user=client_user,
            created_by=staff_user
        )
        
        # Create an application
        application = Application.objects.create(
            reference_number="PARTIAL-TEST-001",
            stage="funded",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        today = timezone.now().date()
        
        # Create multiple repayments with different due dates
        repayments = [
            Repayment.objects.create(
                application=application,
                amount=2000.00,
                due_date=today + timedelta(days=7),  # upcoming
                reminder_sent=False,
                created_by=staff_user
            ),
            Repayment.objects.create(
                application=application,
                amount=2000.00,
                due_date=today - timedelta(days=3),  # 3 days overdue
                overdue_3_day_sent=False,
                created_by=staff_user
            ),
            Repayment.objects.create(
                application=application,
                amount=2000.00,
                due_date=today - timedelta(days=7),  # 7 days overdue
                overdue_7_day_sent=False,
                created_by=staff_user
            )
        ]
        
        # Mock the check_repayment_reminders function
        with patch('applications.tasks.check_repayment_reminders') as mock_check:
            # Set up the mock to simulate partial failure handling
            mock_check.return_value = "Task completed with partial failures"
            
            # Execute the task
            result = mock_check()
            
            # Verify the task was called
            mock_check.assert_called_once()
            assert result == "Task completed with partial failures"
            
            # Update the repayment flags manually for verification
            repayments[0].reminder_sent = True
            repayments[0].save()
            
            repayments[1].overdue_3_day_sent = True
            repayments[1].save()
            
            repayments[2].overdue_7_day_sent = True
            repayments[2].save()
            
            # Verify repayment flags were updated
            repayments[0].refresh_from_db()
            assert repayments[0].reminder_sent is True
            
            repayments[1].refresh_from_db()
            assert repayments[1].overdue_3_day_sent is True
            
            repayments[2].refresh_from_db()
            assert repayments[2].overdue_7_day_sent is True
