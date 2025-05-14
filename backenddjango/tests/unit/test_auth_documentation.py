"""
Test that the authentication API endpoints work as documented in AuthAPIUseCases.md
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthDocumentationTest(TestCase):
    """
    Test that the authentication API endpoints work as documented
    """
    
    def setUp(self):
        """
        Set up test data
        """
        # Create test user
        self.test_user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            role='client',
            first_name='Test',
            last_name='User',
            username='testuser'
        )
        
        # Create API client
        self.api_client = APIClient()
    
    def test_login_success(self):
        """
        Test successful login as documented
        """
        login_url = reverse('login')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.api_client.post(login_url, login_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('role', response.data)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['role'], 'client')
    
    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials as documented
        """
        login_url = reverse('login')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.api_client.post(login_url, login_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')
    
    def test_login_missing_fields(self):
        """
        Test login with missing fields as documented
        """
        login_url = reverse('login')
        login_data = {
            'email': 'testuser@example.com'
            # Missing password field
        }
        response = self.api_client.post(login_url, login_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_success(self):
        """
        Test successful registration as documented
        """
        register_url = reverse('register')
        register_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        response = self.api_client.post(register_url, register_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('role', response.data)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['email'], 'newuser@example.com')
        self.assertEqual(response.data['role'], 'client')
    
    def test_register_email_exists(self):
        """
        Test registration with existing email as documented
        """
        register_url = reverse('register')
        register_data = {
            'email': 'testuser@example.com',  # Already exists
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        response = self.api_client.post(register_url, register_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_register_invalid_role(self):
        """
        Test registration with invalid role as documented
        """
        register_url = reverse('register')
        register_data = {
            'email': 'newuser2@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'invalid_role'  # Invalid role
        }
        response = self.api_client.post(register_url, register_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', response.data)
    
    def test_token_refresh_success(self):
        """
        Test successful token refresh as documented
        """
        # Get a refresh token
        refresh = RefreshToken.for_user(self.test_user)
        
        # Try to refresh the token
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': str(refresh)
        }
        response = self.api_client.post(refresh_url, refresh_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_token_refresh_invalid(self):
        """
        Test token refresh with invalid token as documented
        """
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': 'invalid_token'
        }
        response = self.api_client.post(refresh_url, refresh_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
    
    def test_token_refresh_missing(self):
        """
        Test token refresh with missing token as documented
        """
        refresh_url = reverse('token_refresh')
        refresh_data = {}  # Missing refresh token
        response = self.api_client.post(refresh_url, refresh_data, format='json')
        
        # Verify response matches documentation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response.data)