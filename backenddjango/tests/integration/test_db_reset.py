"""
Test database reset mechanism for integration tests.
Focused on admin user testing.
"""

from django.test import TestCase, TransactionTestCase
from django.db import connection
from django.conf import settings
from users.models import User
from .base import AdminIntegrationTestCase


class DatabaseResetTestCase(AdminIntegrationTestCase):
    """
    Test that the database is reset between test cases.
    This test case uses Django's default TestCase which wraps each test in a transaction.
    """
    
    def test_admin_user_exists(self):
        """
        Test that the admin user created in setUp exists.
        """
        user = User.objects.get(username='admin_test')
        self.assertEqual(user.email, 'admin_test@example.com')
        self.assertTrue(user.is_superuser)
    
    def test_create_another_user(self):
        """
        Test creating another user directly in the database.
        """
        # Create another user directly in the database
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newuserpassword',
            first_name='New',
            last_name='User',
            role='client'
        )
        
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(User.objects.filter(is_superuser=False).count(), 1)


class TransactionDatabaseResetTestCase(TransactionTestCase):
    """
    Test that the database is reset between test cases.
    This test case uses Django's TransactionTestCase which doesn't wrap tests in transactions.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        self.admin_user = User.objects.create_superuser(
            username='admin_transaction',
            email='admin_transaction@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='Transaction',
            role='admin'
        )
    
    def test_admin_user_exists(self):
        """
        Test that the admin user created in setUp exists.
        """
        user = User.objects.get(username='admin_transaction')
        self.assertEqual(user.email, 'admin_transaction@example.com')
        self.assertTrue(user.is_superuser)
    
    def test_create_another_admin(self):
        """
        Test creating another admin user.
        """
        user = User.objects.create_superuser(
            username='admin_transaction2',
            email='admin_transaction2@example.com',
            password='adminpassword',
            first_name='Admin2',
            last_name='Transaction',
            role='admin'
        )
        self.assertTrue(user.is_superuser)
        self.assertEqual(User.objects.filter(is_superuser=True).count(), 2)  # The user from setUp + the new user


class ManualDatabaseResetTestCase(AdminIntegrationTestCase):
    """
    Test manual database reset functionality.
    """
    
    def test_manual_reset(self):
        """
        Test manually resetting the database using DELETE instead of TRUNCATE.
        """
        # Create a user directly in the database
        temp_user = User.objects.create_user(
            username='tempuser',
            email='tempuser@example.com',
            password='tempuserpassword',
            first_name='Temp',
            last_name='User',
            role='client'
        )
        
        # Verify the user exists
        self.assertTrue(User.objects.filter(username='tempuser').exists())
        
        # Manually reset the database by deleting all users
        User.objects.all().delete()
        
        # Verify the user no longer exists
        self.assertFalse(User.objects.filter(username='tempuser').exists())
        self.assertFalse(User.objects.filter(username='admin_test').exists())
