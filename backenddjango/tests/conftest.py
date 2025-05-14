import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from applications.models import Application
from documents.models import Document
from borrowers.models import Borrower
from brokers.models import Broker, Branch, BDM
from users.models import Notification, NotificationPreference
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.fixture
def admin_user():
    """Create an admin user for testing."""
    return User.objects.create_user(
        email='admin@example.com',
        password='password123',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_staff=True,
        is_superuser=True,
        username='admin'  # Add username field
    )


@pytest.fixture
def staff_user():
    """Create a staff user for testing."""
    return User.objects.create_user(
        email='staff@example.com',
        password='password123',
        first_name='Staff',
        last_name='User',
        role='staff',
        username='staff'
    )


@pytest.fixture
def broker_user():
    """Create a broker user for testing."""
    return User.objects.create_user(
        email='broker@example.com',
        password='password123',
        first_name='Broker',
        last_name='User',
        role='broker',
        username='broker'
    )


@pytest.fixture
def client_user():
    """Create a client user for testing."""
    return User.objects.create_user(
        email='client@example.com',
        password='password123',
        first_name='Client',
        last_name='User',
        role='client',
        username='client'
    )


@pytest.fixture
def broker(broker_user):
    """Create a broker for testing."""
    return Broker.objects.create(
        name='Test Broker',
        user=broker_user,
        email='broker@example.com',
        phone='1234567890',
        address='123 Broker St'
    )


@pytest.fixture
def branch():
    """Create a branch for testing."""
    return Branch.objects.create(
        name='Test Branch',
        address='123 Branch St',
        phone='1234567890'
    )


@pytest.fixture
def bdm():
    """Create a BDM for testing."""
    user = User.objects.create_user(
        email='bdm@example.com',
        password='password123',
        first_name='BDM',
        last_name='User',
        role='bd',
        username='bdm'
    )
    return BDM.objects.create(
        user=user,
        name='Test BDM',
        email='bdm@example.com',
        phone='1234567890'
    )


@pytest.fixture
def individual_borrower():
    """Create an individual borrower for testing."""
    return Borrower.objects.create(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        phone='1234567890',
        residential_address='123 Main St',
        borrower_type='individual'
    )


@pytest.fixture
def company_borrower():
    """Create a company borrower for testing."""
    return Borrower.objects.create(
        first_name='Company',
        last_name='Inc',
        email='company@example.com',
        phone='1234567890',
        residential_address='123 Company St',
        is_company=True,
        company_name='Test Company Inc',
        company_abn='12345678901',
        company_acn='123456789',
        company_address='123 Company St'
    )


@pytest.fixture
def application(admin_user, broker, branch, bdm):
    """Create an application for testing."""
    return Application.objects.create(
        reference_number='APP-TEST-001',
        stage='assessment',
        loan_amount=500000,
        loan_term=360,
        interest_rate=4.5,
        purpose='Home purchase',
        application_type='residential',
        broker=broker,
        bd=bdm,
        branch=branch,
        created_by=admin_user
    )


@pytest.fixture
def document_factory(admin_user, application):
    """Factory for creating documents."""
    class DocumentFactory:
        def create(self, **kwargs):
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
            temp_file.write(b'Test file content')
            temp_file.seek(0)
            
            # Default values
            defaults = {
                'title': 'Test Document',
                'description': 'Test description',
                'document_type': 'application_form',
                'application': application,
                'file': SimpleUploadedFile('test.pdf', temp_file.read(), content_type='application/pdf'),
                'file_name': 'test.pdf',
                'file_size': 17,  # Length of 'Test file content'
                'file_type': 'application/pdf',
                'created_by': admin_user
            }
            
            # Override defaults with provided kwargs
            defaults.update(kwargs)
            
            return Document.objects.create(**defaults)
        
        def create_batch(self, count, **kwargs):
            return [self.create(**kwargs) for _ in range(count)]
    
    return DocumentFactory()


@pytest.fixture
def notification(admin_user):
    """Create a notification for testing."""
    return Notification.objects.create(
        user=admin_user,
        title='Test Notification',
        message='This is a test notification',
        notification_type='application_status'
    )


@pytest.fixture
def notification_preference(admin_user):
    """Create notification preferences for testing."""
    return NotificationPreference.objects.create(
        user=admin_user,
        application_status=True,
        document_upload=True,
        repayment_reminder=True,
        email_notifications=True
    )
