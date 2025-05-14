"""
Utility functions for testing.
"""

from unittest.mock import MagicMock, patch
from django.contrib.auth import get_user_model
from django.test import RequestFactory

User = get_user_model()


def create_mock_request(user=None):
    """
    Create a mock request object with an optional user.
    
    Args:
        user: Optional user to attach to the request
        
    Returns:
        A mock request object
    """
    factory = RequestFactory()
    request = factory.get('/')
    
    if user:
        request.user = user
    else:
        request.user = MagicMock(spec=User)
        request.user.is_authenticated = True
        request.user.email = 'mock@example.com'
        request.user.role = 'staff'
    
    return request


def mock_celery_task():
    """
    Create a decorator to mock Celery tasks for testing.
    
    Returns:
        A decorator that can be used to mock Celery tasks
    """
    def decorator(func):
        return patch('celery.app.task')(func)
    return decorator


def mock_aws_s3():
    """
    Create a mock for AWS S3 operations.
    
    Returns:
        A context manager that mocks AWS S3 operations
    """
    class MockS3:
        def __init__(self):
            self.objects = {}
        
        def upload_file(self, file_path, bucket, key):
            self.objects[key] = file_path
            return True
        
        def download_file(self, bucket, key, file_path):
            if key in self.objects:
                return True
            return False
        
        def delete_object(self, bucket, key):
            if key in self.objects:
                del self.objects[key]
                return True
            return False
    
    return patch('boto3.client', return_value=MockS3())


def mock_email_service():
    """
    Create a mock for email service.
    
    Returns:
        A context manager that mocks email sending
    """
    class MockEmailService:
        def __init__(self):
            self.sent_emails = []
        
        def send_email(self, to, subject, body, attachments=None):
            self.sent_emails.append({
                'to': to,
                'subject': subject,
                'body': body,
                'attachments': attachments
            })
            return True
    
    return patch('services.email_service.EmailService', return_value=MockEmailService())
