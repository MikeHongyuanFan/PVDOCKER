import pytest
from django.test import TestCase, override_settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from unittest.mock import patch, MagicMock
from io import BytesIO
from datetime import timedelta

from users.models import User, Notification, NotificationPreference, EmailLog
from users.services import send_email_notification, preview_email
from crm_backend.tasks import send_email_async, send_daily_digest, send_weekly_digest, export_email_logs_to_docx


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class EmailServiceTestCase(TestCase):
    """Test case for email service functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        
        # Create notification preferences
        self.preferences = NotificationPreference.objects.create(
            user=self.user,
            application_status_email=True,
            daily_digest=True,
            weekly_digest=True
        )
        
        # Create test notification
        self.notification = Notification.objects.create(
            user=self.user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='application_status'
        )
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('crm_backend.tasks.send_email_async.delay')
    def test_send_email_notification_plain_text(self, mock_send_email_async):
        """Test sending a plain text email notification"""
        # Configure the mock
        mock_send_email_async.return_value = MagicMock()
        
        # Call the service function
        result = send_email_notification(
            user=self.user,
            subject='Test Subject',
            message='Test Message'
        )
        
        # Check that the task was called with correct parameters
        self.assertTrue(result)
        mock_send_email_async.assert_called_once()
        
        # Check the arguments
        args = mock_send_email_async.call_args[1]
        self.assertEqual(args['subject'], 'Test Subject')
        self.assertEqual(args['message'], 'Test Message')
        self.assertEqual(args['recipient_list'], [self.user.email])
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('crm_backend.tasks.send_email_async.delay')
    def test_send_email_notification_html(self, mock_send_email_async):
        """Test sending an HTML email notification"""
        # Configure the mock
        mock_send_email_async.return_value = MagicMock()
        
        # Mock the render_to_string function
        with patch('users.services.render_to_string') as mock_render:
            mock_render.return_value = '<p>HTML Content</p>'
            
            # Call the service function
            result = send_email_notification(
                user=self.user,
                subject='Test Subject',
                message='Test Message',
                template_name='emails/notification.html',
                context={
                    'subject': 'Test Subject',
                    'message': 'Test Message',
                    'user': self.user
                }
            )
            
            # Check that the task was called with correct parameters
            self.assertTrue(result)
            mock_send_email_async.assert_called_once()
            
            # Check the arguments
            args = mock_send_email_async.call_args[1]
            self.assertEqual(args['subject'], 'Test Subject')
            self.assertEqual(args['user_id'], self.user.id)
            self.assertIsNotNone(args['html_message'])
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('crm_backend.tasks.send_email_async.delay')
    def test_send_email_notification_with_notification(self, mock_send_email_async):
        """Test sending an email notification linked to a notification object"""
        # Configure the mock
        mock_send_email_async.return_value = MagicMock()
        
        # Call the service function
        result = send_email_notification(
            user=self.user,
            subject='Test Subject',
            message='Test Message',
            notification=self.notification
        )
        
        # Check that the task was called with correct parameters
        self.assertTrue(result)
        mock_send_email_async.assert_called_once()
        
        # Check the arguments
        args = mock_send_email_async.call_args[1]
        self.assertEqual(args['subject'], 'Test Subject')
        self.assertEqual(args['notification_id'], self.notification.id)
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_notification_missing_email(self):
        """Test sending an email notification to a user without an email address"""
        # Create a user and then remove their email
        user_no_email = User.objects.create_user(
            email='temp@example.com',
            password='testpassword'
        )
        # Manually set email to empty (bypassing validation)
        User.objects.filter(pk=user_no_email.pk).update(email='')
        user_no_email.refresh_from_db()
        
        # Call the service function
        result = send_email_notification(
            user=user_no_email,
            subject='Test Subject',
            message='Test Message'
        )
        
        # Check that the function returned False
        self.assertFalse(result)
    
    @override_settings(DEBUG=True)
    def test_preview_email(self):
        """Test previewing an email template"""
        # Mock the render_to_string function
        with patch('users.services.render_to_string') as mock_render:
            mock_render.return_value = '<p>HTML Content</p>'
            
            # Call the preview function
            context = {
                'user': self.user,
                'subject': 'Test Subject',
                'message': 'Test Message'
            }
            html_content = preview_email('emails/notification.html', context)
            
            # Check that the template was rendered
            self.assertEqual(html_content, '<p>HTML Content</p>')
            mock_render.assert_called_once_with('emails/notification.html', context)
    
    @override_settings(DEBUG=False)
    def test_preview_email_not_in_debug_mode(self):
        """Test that preview_email raises an error when not in debug mode"""
        context = {
            'user': self.user,
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        
        # Check that the function raises an error
        with self.assertRaises(PermissionError):
            preview_email('emails/notification.html', context)


@pytest.mark.django_db
class TestEmailTasksWithPytest(TestCase):
    """Test case for email-related Celery tasks using pytest with TestCase"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        
        # Create notification preferences
        self.preferences = NotificationPreference.objects.create(
            user=self.user,
            application_status_email=True,
            daily_digest=True,
            weekly_digest=True
        )
        
        # Create test notifications
        self.notifications = []
        for i in range(5):
            notification = Notification.objects.create(
                user=self.user,
                title=f'Test Notification {i}',
                message=f'This is test notification {i}',
                notification_type='application_status',
                is_read=False,
                created_at=timezone.now() - timedelta(hours=i)
            )
            self.notifications.append(notification)
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_async(self):
        """Test the send_email_async task"""
        # Call the task directly (not through Celery)
        with patch('crm_backend.tasks.send_mail') as mock_send_mail:
            mock_send_mail.return_value = 1  # Simulate successful sending
            
            result = send_email_async(
                subject='Test Subject',
                message='Test Message',
                recipient_list=[self.user.email],
                user_id=self.user.id,
                email_type='test'
            )
            
            # Check that send_mail was called
            mock_send_mail.assert_called_once()
            
            # Check that an EmailLog was created
            email_log = EmailLog.objects.filter(user=self.user).first()
            self.assertIsNotNone(email_log)
            self.assertEqual(email_log.subject, 'Test Subject')
            self.assertEqual(email_log.status, 'sent')
            self.assertEqual(email_log.email_type, 'test')
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_async_html(self):
        """Test the send_email_async task with HTML content"""
        # Prepare HTML content
        html_message = '<p>This is <strong>HTML</strong> content</p>'
        
        # Call the task directly (not through Celery)
        with patch('crm_backend.tasks.EmailMultiAlternatives') as mock_email_multi:
            mock_email_instance = MagicMock()
            mock_email_multi.return_value = mock_email_instance
            
            result = send_email_async(
                subject='Test HTML Email',
                message='This is plain text content',
                recipient_list=[self.user.email],
                html_message=html_message,
                user_id=self.user.id
            )
            
            # Check that EmailMultiAlternatives was called
            mock_email_multi.assert_called_once()
            
            # Check that attach_alternative was called with HTML content
            mock_email_instance.attach_alternative.assert_called_once_with(html_message, "text/html")
            
            # Check that send was called
            mock_email_instance.send.assert_called_once()
    
    @override_settings(EMAIL_TEST_MODE=True, EMAIL_TEST_RECIPIENT='test-inbox@example.com')
    def test_send_email_async_test_mode(self):
        """Test the send_email_async task in test mode"""
        # Call the task directly (not through Celery)
        with patch('crm_backend.tasks.send_mail') as mock_send_mail:
            result = send_email_async(
                subject='Test Subject',
                message='Test Message',
                recipient_list=[self.user.email],
                user_id=self.user.id
            )
            
            # Check that send_mail was called with the test recipient
            mock_send_mail.assert_called_once()
            args, kwargs = mock_send_mail.call_args
            self.assertEqual(kwargs['recipient_list'], ['test-inbox@example.com'])
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_daily_digest(self):
        """Test the send_daily_digest task"""
        # Mock render_to_string to avoid template not found error
        with patch('django.template.loader.get_template') as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = '<p>Daily Digest Content</p>'
            mock_get_template.return_value = mock_template
            
            # Mock send_email_async to avoid actual sending
            with patch('crm_backend.tasks.send_email_async.delay') as mock_send:
                # Call the task directly (not through Celery)
                send_daily_digest()
                
                # Check that send_email_async was called
                mock_send.assert_called()
                
                # Check that the email was sent to the correct user
                args, kwargs = mock_send.call_args
                self.assertEqual(kwargs['recipient_list'], [self.user.email])
                self.assertIn('Daily Digest', kwargs['subject'])
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_weekly_digest(self):
        """Test the send_weekly_digest task"""
        # Mock render_to_string to avoid template not found error
        with patch('django.template.loader.get_template') as mock_get_template:
            mock_template = MagicMock()
            mock_template.render.return_value = '<p>Weekly Digest Content</p>'
            mock_get_template.return_value = mock_template
            
            # Mock send_email_async to avoid actual sending
            with patch('crm_backend.tasks.send_email_async.delay') as mock_send:
                # Call the task directly (not through Celery)
                send_weekly_digest()
                
                # Check that send_email_async was called
                mock_send.assert_called()
                
                # Check that the email was sent to the correct user
                args, kwargs = mock_send.call_args
                self.assertEqual(kwargs['recipient_list'], [self.user.email])
                self.assertIn('Weekly Digest', kwargs['subject'])
    
    def test_export_email_logs_to_docx(self):
        """Test the export_email_logs_to_docx task"""
        # Create some email logs
        email_logs = []
        for i in range(3):
            log = EmailLog.objects.create(
                user=self.user,
                subject=f'Test Email {i}',
                message_body=f'This is test email {i}',
                status='sent',
                email_type='test'
            )
            email_logs.append(log)
        
        # Get the IDs
        log_ids = [log.id for log in email_logs]
        
        # Mock Document class to avoid actual file creation
        with patch('crm_backend.tasks.Document') as mock_document:
            mock_doc_instance = MagicMock()
            mock_document.return_value = mock_doc_instance
            
            # Mock BytesIO
            mock_output = MagicMock(spec=BytesIO)
            with patch('crm_backend.tasks.BytesIO', return_value=mock_output):
                # Call the task directly (not through Celery)
                output = export_email_logs_to_docx(log_ids)
                
                # Check that Document was created
                mock_document.assert_called_once()
                
                # Check that the document was saved
                mock_doc_instance.save.assert_called_once()
                
                # Check that a BytesIO object was returned
                self.assertIs(output, mock_output)
