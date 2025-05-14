"""
Unit tests for notification services.
"""

import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from users.models import Notification, NotificationPreference
from users.services import (
    create_notification,
    create_application_notification,
    send_email_notification,
    get_or_create_notification_preferences
)
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, BDM

User = get_user_model()


@pytest.mark.django_db
class TestNotificationService:
    """Test the notification service."""
    
    def test_create_notification(self, client_user):
        """Test creating a notification."""
        # Create notification
        notification = create_notification(
            user=client_user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="system"
        )
        
        # Verify notification was created
        assert notification is not None
        assert notification.user == client_user
        assert notification.title == "Test Notification"
        assert notification.message == "This is a test notification"
        assert notification.notification_type == "system"
        assert notification.is_read is False
    
    def test_create_notification_with_preferences_disabled(self, client_user):
        """Test creating a notification when preferences are disabled."""
        # Create notification preferences with in-app notifications disabled for system type
        preferences = NotificationPreference.objects.create(
            user=client_user,
            system_in_app=False
        )
        
        # Create notification
        notification = create_notification(
            user=client_user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="system"
        )
        
        # Verify notification was not created
        assert notification is None
        assert Notification.objects.filter(user=client_user).count() == 0
    
    def test_create_notification_with_related_object(self, client_user):
        """Test creating a notification with a related object."""
        # Create notification
        notification = create_notification(
            user=client_user,
            title="Test Notification",
            message="This is a test notification",
            notification_type="system",
            related_object_id=123,
            related_object_type="application"
        )
        
        # Verify notification was created with related object
        assert notification is not None
        assert notification.related_object_id == 123
        assert notification.related_object_type == "application"
    
    def test_create_notification_websocket(self, client_user):
        """Test creating a notification sends WebSocket message."""
        # Mock channel layer
        with patch('users.services.get_channel_layer') as mock_channel_layer, \
             patch('users.services.async_to_sync') as mock_async_to_sync:
            
            mock_channel = MagicMock()
            mock_channel_layer.return_value = mock_channel
            mock_async_func = MagicMock()
            mock_async_to_sync.return_value = mock_async_func
            
            # Create notification
            notification = create_notification(
                user=client_user,
                title="Test Notification",
                message="This is a test notification",
                notification_type="system"
            )
            
            # Verify WebSocket message was sent
            assert mock_async_to_sync.call_count >= 1
            assert mock_async_func.call_count >= 1
    
    def test_create_notification_email(self, client_user):
        """Test creating a notification sends email."""
        # Create notification preferences with email notifications enabled for system type
        preferences = NotificationPreference.objects.create(
            user=client_user,
            system_email=True
        )
        
        # Mock send_mail
        with patch('users.services.send_mail') as mock_send_mail:
            # Create notification
            notification = create_notification(
                user=client_user,
                title="Test Notification",
                message="This is a test notification",
                notification_type="system"
            )
            
            # Verify email was sent
            mock_send_mail.assert_called_once()
            args, kwargs = mock_send_mail.call_args
            assert kwargs['subject'] == "Test Notification"
            assert kwargs['message'] == "This is a test notification"
            assert kwargs['recipient_list'] == [client_user.email]
    
    def test_create_application_notification(self, staff_user, broker_user, client_user, admin_user):
        """Test creating notifications for users related to an application."""
        # Create a borrower with user account
        borrower = Borrower.objects.create(
            first_name="Test",
            last_name="Borrower",
            email=client_user.email,
            user=client_user,
            created_by=client_user
        )
        
        # Create application directly
        application = Application.objects.create(
            reference_number="APP-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(borrower)
        
        # Mock the notification creation to avoid WebSocket issues
        with patch('users.services.create_notification') as mock_create_notification:
            mock_create_notification.return_value = MagicMock()
            
            # Create application notification
            notifications = create_application_notification(
                application=application,
                notification_type="application_status",
                title="Application Status Changed",
                message="The application status has changed to Assessment"
            )
            
            # Verify create_notification was called for admin users
            admin_call = False
            for call in mock_create_notification.call_args_list:
                args, kwargs = call
                if kwargs.get('user') == admin_user:
                    admin_call = True
                    assert kwargs.get('title') == "Application Status Changed"
                    assert kwargs.get('message') == "The application status has changed to Assessment"
                    assert kwargs.get('notification_type') == "application_status"
                    assert kwargs.get('related_object_id') == application.id
                    assert kwargs.get('related_object_type') == "application"
            
            assert admin_call, "No notification was created for admin user"
    
    def test_send_email_notification(self, client_user):
        """Test sending an email notification."""
        # Mock send_mail
        with patch('users.services.send_mail') as mock_send_mail:
            # Send email notification
            result = send_email_notification(
                user=client_user,
                subject="Test Email",
                message="This is a test email"
            )
            
            # Verify email was sent
            assert result is True
            mock_send_mail.assert_called_once()
            args, kwargs = mock_send_mail.call_args
            assert kwargs['subject'] == "Test Email"
            assert kwargs['message'] == "This is a test email"
            assert kwargs['recipient_list'] == [client_user.email]
    
    def test_send_email_notification_no_email(self):
        """Test sending an email notification to a user with no email."""
        # Create user with no email
        user = User.objects.create(
            username="noemail",
            email=""
        )
        
        # Send email notification
        result = send_email_notification(
            user=user,
            subject="Test Email",
            message="This is a test email"
        )
        
        # Verify email was not sent
        assert result is False
    
    def test_send_email_notification_error(self, client_user):
        """Test sending an email notification with an error."""
        # Mock send_mail to raise an exception
        with patch('users.services.send_mail', side_effect=Exception("Email error")):
            # Send email notification
            result = send_email_notification(
                user=client_user,
                subject="Test Email",
                message="This is a test email"
            )
            
            # Verify result indicates failure
            assert result is False
    
    def test_get_or_create_notification_preferences_existing(self, client_user):
        """Test getting existing notification preferences."""
        # Create notification preferences
        original_preferences = NotificationPreference.objects.create(
            user=client_user,
            system_in_app=False,
            system_email=True
        )
        
        # Get or create preferences
        preferences = get_or_create_notification_preferences(client_user)
        
        # Verify existing preferences were returned
        assert preferences.id == original_preferences.id
        assert preferences.system_in_app is False
        assert preferences.system_email is True
    
    def test_get_or_create_notification_preferences_new(self, client_user):
        """Test creating new notification preferences."""
        # Get or create preferences
        preferences = get_or_create_notification_preferences(client_user)
        
        # Verify new preferences were created with defaults
        assert preferences is not None
        assert preferences.system_in_app is True  # Default value
        assert preferences.system_email is False  # Default value
        
        # Verify preferences were saved to database
        assert NotificationPreference.objects.filter(user=client_user).exists()


@pytest.mark.django_db
class TestNotificationServiceWithRealEmail:
    """Test the notification service with real email sending."""
    
    def test_send_real_email_notification(self):
        """Test sending a real email notification."""
        # Create a test user with the specified email
        user = User.objects.create(
            username="testuser",
            email="fanhongyuan897@gmail.com"
        )
        
        # Send a real email notification
        result = send_email_notification(
            user=user,
            subject="Test Email from CRM Loan Management System",
            message="This is a test email sent during the WebSocket testing phase. "
                   "If you're receiving this, the email notification system is working correctly."
        )
        
        # Verify the result (this doesn't guarantee delivery, just that no errors occurred)
        assert result is True
