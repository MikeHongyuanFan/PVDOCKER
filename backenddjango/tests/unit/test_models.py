"""
Unit tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from applications.models import Application
from borrowers.models import Borrower
from brokers.models import Broker, Branch, BDM
from documents.models import Document
from users.models import Notification

User = get_user_model()


class UserModelTest(TestCase):
    """
    Test the User model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='staff'
        )
    
    def test_user_creation(self):
        """
        Test that a user can be created.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.role, 'staff')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_str(self):
        """
        Test the string representation of a user.
        """
        self.assertEqual(str(self.user), 'test@example.com')
    
    def test_get_full_name(self):
        """
        Test the get_full_name method.
        """
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_get_short_name(self):
        """
        Test the get_short_name method.
        """
        self.assertEqual(self.user.get_short_name(), 'Test')


class BorrowerModelTest(TestCase):
    """
    Test the Borrower model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            residential_address='123 Test St',
            date_of_birth='1980-01-01',
            employment_type='full_time',
            annual_income=75000,
            created_by=self.user
        )
    
    def test_borrower_creation(self):
        """
        Test that a borrower can be created.
        """
        self.assertEqual(self.borrower.first_name, 'John')
        self.assertEqual(self.borrower.last_name, 'Doe')
        self.assertEqual(self.borrower.email, 'john.doe@example.com')
        self.assertEqual(self.borrower.phone, '1234567890')
        self.assertEqual(self.borrower.residential_address, '123 Test St')
        self.assertEqual(str(self.borrower.date_of_birth), '1980-01-01')
        self.assertEqual(self.borrower.employment_type, 'full_time')
        self.assertEqual(self.borrower.annual_income, 75000)
        self.assertEqual(self.borrower.created_by, self.user)
    
    def test_borrower_str(self):
        """
        Test the string representation of a borrower.
        """
        self.assertEqual(str(self.borrower), 'John Doe')
    
    def test_borrower_company_str(self):
        """
        Test the string representation of a company borrower.
        """
        company_borrower = Borrower.objects.create(
            is_company=True,
            company_name='Test Company Ltd',
            created_by=self.user
        )
        self.assertEqual(str(company_borrower), 'Test Company Ltd')


class BranchModelTest(TestCase):
    """
    Test the Branch model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='456 Branch St',
            phone='0987654321',
            email='branch@example.com',
            created_by=self.user
        )
    
    def test_branch_creation(self):
        """
        Test that a branch can be created.
        """
        self.assertEqual(self.branch.name, 'Test Branch')
        self.assertEqual(self.branch.address, '456 Branch St')
        self.assertEqual(self.branch.phone, '0987654321')
        self.assertEqual(self.branch.email, 'branch@example.com')
        self.assertEqual(self.branch.created_by, self.user)
    
    def test_branch_str(self):
        """
        Test the string representation of a branch.
        """
        self.assertEqual(str(self.branch), 'Test Branch')


class BrokerModelTest(TestCase):
    """
    Test the Broker model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.broker_user = User.objects.create_user(
            username='brokeruser',
            email='broker@example.com',
            password='brokerpass123',
            role='broker'
        )
        
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='456 Branch St',
            phone='0987654321',
            email='branch@example.com',
            created_by=self.user
        )
        
        self.broker = Broker.objects.create(
            name='Test Broker',
            company='Test Company',
            email='broker@testcompany.com',
            phone='1122334455',
            address='789 Broker St',
            branch=self.branch,
            user=self.broker_user,
            commission_bank_name='Test Bank',
            commission_account_name='Test Broker',
            commission_account_number='123456789',
            commission_bsb='123456',
            created_by=self.user
        )
    
    def test_broker_creation(self):
        """
        Test that a broker can be created.
        """
        self.assertEqual(self.broker.name, 'Test Broker')
        self.assertEqual(self.broker.company, 'Test Company')
        self.assertEqual(self.broker.email, 'broker@testcompany.com')
        self.assertEqual(self.broker.phone, '1122334455')
        self.assertEqual(self.broker.address, '789 Broker St')
        self.assertEqual(self.broker.branch, self.branch)
        self.assertEqual(self.broker.user, self.broker_user)
        self.assertEqual(self.broker.commission_bank_name, 'Test Bank')
        self.assertEqual(self.broker.commission_account_name, 'Test Broker')
        self.assertEqual(self.broker.commission_account_number, '123456789')
        self.assertEqual(self.broker.commission_bsb, '123456')
        self.assertEqual(self.broker.created_by, self.user)
    
    def test_broker_str(self):
        """
        Test the string representation of a broker.
        """
        self.assertEqual(str(self.broker), f"{self.broker.name} ({self.broker.company})")


class BDMModelTest(TestCase):
    """
    Test the BDM model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            role='staff'
        )
        
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='456 Branch St',
            phone='0987654321',
            email='branch@example.com',
            created_by=self.user
        )
        
        self.bdm = BDM.objects.create(
            name='Test BDM',
            email='bdm@example.com',
            phone='5566778899',
            branch=self.branch,
            user=self.staff_user,
            created_by=self.user
        )
    
    def test_bdm_creation(self):
        """
        Test that a BDM can be created.
        """
        self.assertEqual(self.bdm.name, 'Test BDM')
        self.assertEqual(self.bdm.email, 'bdm@example.com')
        self.assertEqual(self.bdm.phone, '5566778899')
        self.assertEqual(self.bdm.branch, self.branch)
        self.assertEqual(self.bdm.user, self.staff_user)
        self.assertEqual(self.bdm.created_by, self.user)
    
    def test_bdm_str(self):
        """
        Test the string representation of a BDM.
        """
        self.assertEqual(str(self.bdm), 'Test BDM')


class NotificationModelTest(TestCase):
    """
    Test the Notification model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notification = Notification.objects.create(
            user=self.user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='info'
        )
    
    def test_notification_creation(self):
        """
        Test that a notification can be created.
        """
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.message, 'This is a test notification')
        self.assertEqual(self.notification.notification_type, 'info')
        self.assertFalse(self.notification.is_read)
    
    def test_notification_str(self):
        """
        Test the string representation of a notification.
        """
        self.assertEqual(str(self.notification), f"{self.notification.notification_type}: {self.notification.title}")
    
    def test_mark_as_read(self):
        """
        Test the mark_as_read method.
        """
        self.notification.mark_as_read()
        self.assertTrue(self.notification.is_read)
        self.assertIsNotNone(self.notification.read_at)
