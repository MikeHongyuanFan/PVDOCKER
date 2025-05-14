"""
Unit tests for serializers.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from borrowers.models import Borrower
from borrowers.serializers import BorrowerSerializer
from users.serializers import UserSerializer
from brokers.serializers import BrokerSerializer, BranchSerializer
from brokers.models import Broker, Branch

User = get_user_model()


class UserSerializerTest(TestCase):
    """
    Test the UserSerializer.
    """
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'staff'
        }
        
        self.user = User.objects.create_user(**self.user_data)
        self.serializer = UserSerializer(instance=self.user)
    
    def test_contains_expected_fields(self):
        """
        Test that the serializer contains the expected fields.
        """
        data = self.serializer.data
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertIn('email', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('role', data)
        self.assertIn('date_joined', data)
        self.assertNotIn('password', data)  # Password should not be included
    
    def test_field_content(self):
        """
        Test that the serializer fields contain the expected values.
        """
        data = self.serializer.data
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['role'], 'staff')


class BorrowerSerializerTest(TestCase):
    """
    Test the BorrowerSerializer.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.borrower_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'address': '123 Test St',
            'date_of_birth': '1980-01-01',
            'employment_status': 'Employed',
            'annual_income': 75000,
            'created_by': self.user
        }
        
        self.borrower = Borrower.objects.create(**self.borrower_data)
        self.serializer = BorrowerSerializer(instance=self.borrower)
    
    def test_contains_expected_fields(self):
        """
        Test that the serializer contains the expected fields.
        """
        data = self.serializer.data
        self.assertIn('id', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('email', data)
        self.assertIn('phone', data)
        self.assertIn('address', data)
        self.assertIn('date_of_birth', data)
        self.assertIn('employment_status', data)
        self.assertIn('annual_income', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_field_content(self):
        """
        Test that the serializer fields contain the expected values.
        """
        data = self.serializer.data
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertEqual(data['phone'], '1234567890')
        self.assertEqual(data['address'], '123 Test St')
        self.assertEqual(data['date_of_birth'], '1980-01-01')
        self.assertEqual(data['employment_status'], 'Employed')
        self.assertEqual(data['annual_income'], '75000.00')  # Note: Decimal is serialized as string


class BranchSerializerTest(TestCase):
    """
    Test the BranchSerializer.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.branch_data = {
            'name': 'Test Branch',
            'address': '456 Branch St',
            'phone': '0987654321',
            'email': 'branch@example.com',
            'created_by': self.user
        }
        
        self.branch = Branch.objects.create(**self.branch_data)
        self.serializer = BranchSerializer(instance=self.branch)
    
    def test_contains_expected_fields(self):
        """
        Test that the serializer contains the expected fields.
        """
        data = self.serializer.data
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('address', data)
        self.assertIn('phone', data)
        self.assertIn('email', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_field_content(self):
        """
        Test that the serializer fields contain the expected values.
        """
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Branch')
        self.assertEqual(data['address'], '456 Branch St')
        self.assertEqual(data['phone'], '0987654321')
        self.assertEqual(data['email'], 'branch@example.com')


class BrokerSerializerTest(TestCase):
    """
    Test the BrokerSerializer.
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
        
        self.broker_data = {
            'name': 'Test Broker',
            'company': 'Test Company',
            'email': 'broker@testcompany.com',
            'phone': '1122334455',
            'address': '789 Broker St',
            'branch': self.branch,
            'user': self.broker_user,
            'commission_bank_name': 'Test Bank',
            'commission_account_name': 'Test Broker',
            'commission_account_number': '123456789',
            'commission_bsb': '123456',
            'created_by': self.user
        }
        
        self.broker = Broker.objects.create(**self.broker_data)
        self.serializer = BrokerSerializer(instance=self.broker)
    
    def test_contains_expected_fields(self):
        """
        Test that the serializer contains the expected fields.
        """
        data = self.serializer.data
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('company', data)
        self.assertIn('email', data)
        self.assertIn('phone', data)
        self.assertIn('address', data)
        self.assertIn('branch', data)
        self.assertIn('user', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_field_content(self):
        """
        Test that the serializer fields contain the expected values.
        """
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Broker')
        self.assertEqual(data['company'], 'Test Company')
        self.assertEqual(data['email'], 'broker@testcompany.com')
        self.assertEqual(data['phone'], '1122334455')
        self.assertEqual(data['address'], '789 Broker St')
        self.assertEqual(data['branch'], self.branch.id)
        self.assertEqual(data['user'], self.broker_user.id)
