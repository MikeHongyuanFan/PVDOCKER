"""
Test admin authentication for integration tests.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class AdminAuthenticationTest(TestCase):
    """
    Test admin authentication for integration tests.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin_auth',
            email='admin_auth@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='Auth',
            role='admin'
        )
    
    def test_jwt_token_auth(self):
        """
        Test JWT token authentication for admin user.
        """
        # Get token directly
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        
        # Test authentication with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Try to access user profile
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'admin_auth@example.com')
    
    def test_authenticated_access(self):
        """
        Test accessing protected endpoint with authentication.
        """
        # Get token
        refresh = RefreshToken.for_user(self.admin_user)
        access_token = str(refresh.access_token)
        
        # Access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'admin_auth@example.com')
    
    def test_unauthenticated_access(self):
        """
        Test accessing protected endpoint without authentication.
        """
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_token(self):
        """
        Test that invalid tokens are rejected.
        """
        # Use an invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
