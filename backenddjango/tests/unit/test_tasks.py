"""
Unit tests for Celery tasks.
"""

import pytest
from unittest.mock import patch, MagicMock
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


@pytest.mark.django_db
class TestStaleApplicationsTask:
    """Test the stale applications check task."""
    
    def test_check_stale_applications(self, staff_user, broker_user):
        """Test checking for stale applications."""
        # Create a BDM profile for the staff user
        from brokers.models import BDM, Branch
        branch = Branch.objects.create(
            name="Test Branch",
            created_by=staff_user
        )
        bdm = BDM.objects.create(
            name="Test BDM",
            email=staff_user.email,
            user=staff_user,
            branch=branch,
            created_by=staff_user
        )
        
        # Create a broker profile for the broker user
        from brokers.models import Broker
        broker = Broker.objects.create(
            name="Test Broker",
            email=broker_user.email,
            user=broker_user,
            branch=branch,
            created_by=staff_user
        )
        
        # Create a stale application (older than threshold)
        stale_date = timezone.now() - timedelta(days=20)
        stale_app = Application.objects.create(
            reference_number="STALE-001",
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
        
        # Manually update the timestamps to make it stale
        Application.objects.filter(id=stale_app.id).update(
            created_at=stale_date,
            updated_at=stale_date
        )
        
        # Create a recent application (not stale)
        recent_app = Application.objects.create(
            reference_number="RECENT-001",
            stage="assessment",
            loan_amount=600000,
            loan_term=360,
            interest_rate=4.2,
            purpose="Home purchase",
            application_type="residential",
            created_by=broker_user,
            broker=broker,
            bd=bdm
        )
        
        # Create a completed application (should be excluded)
        completed_app = Application.objects.create(
            reference_number="COMPLETE-001",
            stage="funded",
            loan_amount=700000,
            loan_term=360,
            interest_rate=4.0,
            purpose="Home purchase",
            application_type="residential",
            created_by=broker_user,
            broker=broker,
            bd=bdm
        )
        Application.objects.filter(id=completed_app.id).update(
            created_at=stale_date,
            updated_at=stale_date
        )
        
        # Mock the send_mail function
        with patch('applications.tasks.send_mail') as mock_send_mail:
            # Run the task
            check_stale_applications()
            
            # Verify email was sent for stale application only
            assert mock_send_mail.call_count == 1
            
            # Check email content
            args, kwargs = mock_send_mail.call_args
            assert f'Stale Application Alert: {stale_app.reference_number}' in kwargs['subject']
            assert stale_app.reference_number in kwargs['message']
            assert staff_user.email in kwargs['recipient_list']
            
            # Verify no email for recent or completed applications
            for call in mock_send_mail.call_args_list:
                _, call_kwargs = call
                assert recent_app.reference_number not in call_kwargs['message']
                assert completed_app.reference_number not in call_kwargs['message']


@pytest.mark.django_db
class TestNoteRemindersTask:
    """Test the note reminders check task."""
    
    def test_check_note_reminders(self, staff_user):
        """Test checking for note reminders."""
        # Create an application
        application = Application.objects.create(
            reference_number="NOTE-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Create a note with today's reminder date
        today = timezone.now().date()
        reminder_note = Note.objects.create(
            title="Reminder Note",
            content="This note has a reminder for today",
            application=application,
            remind_date=today,
            created_by=staff_user
        )
        
        # Create a note with future reminder date
        future_note = Note.objects.create(
            title="Future Note",
            content="This note has a reminder for the future",
            application=application,
            remind_date=today + timedelta(days=7),
            created_by=staff_user
        )
        
        # Create a note with past reminder date
        past_note = Note.objects.create(
            title="Past Note",
            content="This note had a reminder in the past",
            application=application,
            remind_date=today - timedelta(days=7),
            created_by=staff_user
        )
        
        # Mock the send_mail function
        with patch('applications.tasks.send_mail') as mock_send_mail:
            # Run the task
            check_note_reminders()
            
            # Verify email was sent for today's reminder only
            assert mock_send_mail.call_count == 1
            
            # Check email content
            args, kwargs = mock_send_mail.call_args
            assert f'Note Reminder: {reminder_note.title}' in kwargs['subject']
            assert reminder_note.content in kwargs['message']
            assert staff_user.email in kwargs['recipient_list']
            
            # Verify no email for future or past notes
            for call in mock_send_mail.call_args_list:
                _, call_kwargs = call
                assert future_note.title not in call_kwargs['subject']
                assert past_note.title not in call_kwargs['subject']


@pytest.mark.django_db
class TestRepaymentRemindersTask:
    """Test the repayment reminders check task."""
    
    def test_check_repayment_reminders(self, staff_user, client_user):
        """Test checking for repayment reminders."""
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Repayment",
            last_name="Test",
            email=client_user.email,
            user=client_user,
            created_by=staff_user
        )
        
        # Create a BDM profile for the staff user
        from brokers.models import BDM, Branch
        branch = Branch.objects.create(
            name="Test Branch",
            created_by=staff_user
        )
        bdm = BDM.objects.create(
            name="Test BDM",
            email=staff_user.email,
            user=staff_user,
            branch=branch,
            created_by=staff_user
        )
        
        # Create an application
        application = Application.objects.create(
            reference_number="REPAY-TEST-001",
            stage="funded",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user,
            bd=bdm
        )
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        today = timezone.now().date()
        
        # Create upcoming repayment (due in 7 days)
        upcoming_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today + timedelta(days=7),
            reminder_sent=False,
            created_by=staff_user
        )
        
        # Create 3-day overdue repayment
        overdue_3_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today - timedelta(days=3),
            overdue_3_day_sent=False,
            created_by=staff_user
        )
        
        # Create 7-day overdue repayment
        overdue_7_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today - timedelta(days=7),
            overdue_7_day_sent=False,
            created_by=staff_user
        )
        
        # Create 10-day overdue repayment
        overdue_10_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today - timedelta(days=10),
            overdue_10_day_sent=False,
            created_by=staff_user
        )
        
        # Mock the send_mail function
        with patch('applications.tasks.send_mail') as mock_send_mail:
            # Run the task
            check_repayment_reminders()
            
            # Verify emails were sent for all repayments
            assert mock_send_mail.call_count == 4
            
            # Check that repayments were marked as notified
            upcoming_repayment.refresh_from_db()
            assert upcoming_repayment.reminder_sent is True
            
            overdue_3_repayment.refresh_from_db()
            assert overdue_3_repayment.overdue_3_day_sent is True
            
            overdue_7_repayment.refresh_from_db()
            assert overdue_7_repayment.overdue_7_day_sent is True
            
            overdue_10_repayment.refresh_from_db()
            assert overdue_10_repayment.overdue_10_day_sent is True
            
            # Verify email content and recipients
            email_subjects = [call[1]['subject'] for call in mock_send_mail.call_args_list]
            assert 'Upcoming Repayment Reminder' in email_subjects
            assert 'OVERDUE Repayment Notice' in email_subjects
            assert 'URGENT: 7 Days OVERDUE Repayment' in email_subjects
            assert 'ESCALATION: 10 Days Overdue Repayment' in email_subjects
            
            # Check that borrower received notifications for first 3 cases
            borrower_emails = 0
            bdm_emails = 0
            for call in mock_send_mail.call_args_list:
                _, call_kwargs = call
                if client_user.email in call_kwargs['recipient_list']:
                    borrower_emails += 1
                if staff_user.email in call_kwargs['recipient_list']:
                    bdm_emails += 1
            
            assert borrower_emails == 3  # Upcoming, 3-day, and 7-day notices
            assert bdm_emails == 1  # 10-day escalation
    
    def test_check_repayment_reminders_already_sent(self, staff_user, client_user):
        """Test checking for repayment reminders that were already sent."""
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Already",
            last_name="Sent",
            email=client_user.email,
            user=client_user,
            created_by=staff_user
        )
        
        # Create an application
        application = Application.objects.create(
            reference_number="ALREADY-SENT-001",
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
        
        # Create upcoming repayment with reminder already sent
        upcoming_repayment = Repayment.objects.create(
            application=application,
            amount=2000.00,
            due_date=today + timedelta(days=7),
            reminder_sent=True,  # Already sent
            created_by=staff_user
        )
        
        # Mock the send_mail function
        with patch('applications.tasks.send_mail') as mock_send_mail:
            # Run the task
            check_repayment_reminders()
            
            # Verify no emails were sent
            assert mock_send_mail.call_count == 0
