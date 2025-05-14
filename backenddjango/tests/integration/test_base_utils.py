"""
Test the base utilities for integration tests.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from .base import AdminIntegrationTestCase
from .utils.auth_utils import create_admin_user, get_tokens_for_user
from .utils.request_utils import build_url
from .utils.response_utils import get_response_data
from .utils.file_utils import create_text_file
from .utils.data_utils import random_string, random_email


class BaseUtilsTest(TestCase):
    """
    Test the base utilities for integration tests.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        self.client = APIClient()
        self.admin_user = create_admin_user()
    
    def test_auth_utils(self):
        """
        Test the authentication utilities.
        """
        # Test create_admin_user
        self.assertTrue(self.admin_user.is_superuser)
        self.assertEqual(self.admin_user.role, 'admin')
        
        # Test get_tokens_for_user
        access_token, refresh_token = get_tokens_for_user(self.admin_user)
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)
    
    def test_request_utils(self):
        """
        Test the request utilities.
        """
        # Test build_url
        url = build_url('user-list')
        self.assertEqual(url, reverse('user-list'))
        
        # Test build_url with pk
        url = build_url('user-detail', pk=1)
        self.assertEqual(url, reverse('user-detail', args=[1]))
        
        # Test build_url with query params
        url = build_url('user-list', query_params={'search': 'test'})
        self.assertEqual(url, reverse('user-list') + '?search=test')
    
    def test_response_utils(self):
        """
        Test the response utils.
        """
        # Authenticate
        access_token, _ = get_tokens_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Make a request
        response = self.client.get(reverse('user-detail', args=[self.admin_user.id]))
        
        # Test get_response_data
        data = get_response_data(response)
        self.assertIsNotNone(data)
        self.assertEqual(data['email'], self.admin_user.email)
    
    def test_file_utils(self):
        """
        Test the file utilities.
        """
        # Test create_text_file
        file = create_text_file(content="Test content", filename="test.txt")
        self.assertEqual(file.name, "test.txt")
        self.assertEqual(file.read(), b"Test content")
    
    def test_data_utils(self):
        """
        Test the data utilities.
        """
        # Test random_string
        string = random_string(10)
        self.assertEqual(len(string), 10)
        
        # Test random_email
        email = random_email()
        self.assertIn('@', email)


class AdminIntegrationTestCaseTest(AdminIntegrationTestCase):
    """
    Test the AdminIntegrationTestCase base class.
    """
    
    def test_admin_user_setup(self):
        """
        Test that the admin user is set up correctly.
        """
        self.assertTrue(self.admin_user.is_superuser)
        self.assertEqual(self.admin_user.role, 'admin')
    
    def test_authentication(self):
        """
        Test that authentication works correctly.
        """
        # Test that we're authenticated
        response = self.client.get(reverse('user-detail', args=[self.admin_user.id]))
        self.assert_status_code(response, status.HTTP_200_OK)
        
        # Test clear_authentication
        self.clear_authentication()
        response = self.client.get(reverse('user-detail', args=[self.admin_user.id]))
        self.assert_status_code(response, status.HTTP_401_UNAUTHORIZED)
        
        # Test refresh_authentication
        self.refresh_authentication()
        response = self.client.get(reverse('user-detail', args=[self.admin_user.id]))
        self.assert_status_code(response, status.HTTP_200_OK)
    
    def test_api_helpers(self):
        """
        Test the API helper methods.
        """
        # Test get_api
        response = self.get_api('user-detail', pk=self.admin_user.id)
        self.assert_response_contains(response, 'email', self.admin_user.email)
        
        # Create a new user for testing
        new_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        
        # Test post_api
        response = self.post_api('user-list', new_user_data)
        self.assert_response_contains(response, 'email', 'newuser@example.com')
        
        # Get the new user's ID
        new_user_id = response.data['id']
        
        # Test patch_api
        patch_data = {'last_name': 'Patched'}
        response = self.patch_api('user-detail', patch_data, pk=new_user_id)
        self.assert_response_contains(response, 'last_name', 'Patched')
        
        # Test delete_api
        self.delete_api('user-detail', pk=new_user_id)
        
        # Verify the user was deleted
        self.assert_object_does_not_exist(User, id=new_user_id)
    
    def test_assertion_helpers(self):
        """
        Test the assertion helper methods.
        """
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testuserpassword',
            first_name='Test',
            last_name='User',
            role='client'
        )
        
        # Test assert_object_exists
        self.assert_object_exists(User, username='testuser')
        
        # Test assert_object_count
        initial_count = User.objects.count()
        self.assert_object_count(User, initial_count)
        
        # Create another user
        User.objects.create_user(
            username='anotheruser',
            email='anotheruser@example.com',
            password='anotheruserpassword',
            first_name='Another',
            last_name='User',
            role='client'
        )
        
        # Test assert_object_count again
        self.assert_object_count(User, initial_count + 1)
