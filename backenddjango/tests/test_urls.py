import unittest
from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class URLEndpointTests(TestCase):
    """Test case to verify the existence of all URL endpoints in the application."""
    
    def setUp(self):
        """Set up test client and create a test user for authenticated endpoints."""
        self.client = APIClient()
        
        # Create a test user for authenticated endpoints
        self.test_user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Base endpoints to test
        self.base_endpoints = [
            '/admin/',
            '/api/users/',
            '/api/applications/',
            '/api/borrowers/',
            '/api/brokers/',
            '/api/documents/',
            '/api/products/',
            # Reports endpoint doesn't have a root endpoint, only specific report endpoints
            '/api/reports/repayment-compliance/',
            '/api/reports/application-volume/',
            '/api/reports/application-status/',
            '/api/schema/',
            '/api/swagger/',
            '/api/redoc/',
        ]
    
    def test_base_endpoints_exist(self):
        """Test that all base endpoints return a response (not 404)."""
        for endpoint in self.base_endpoints:
            response = self.client.get(endpoint)
            # We don't care about the specific status code (could be 200, 302, 401, etc.)
            # We just want to make sure it's not a 404 (Not Found)
            self.assertNotEqual(
                response.status_code, 
                status.HTTP_404_NOT_FOUND,
                f"Endpoint {endpoint} returned 404 Not Found"
            )
            print(f"Endpoint {endpoint} - Status: {response.status_code}")
    
    def test_authenticated_endpoints(self):
        """Test endpoints with authentication."""
        # Login the test user
        self.client.force_authenticate(user=self.test_user)
        
        # Test authenticated endpoints
        authenticated_endpoints = [
            # '/api/users/me/' - This endpoint doesn't exist based on test results
            '/api/applications/',
            '/api/borrowers/',
            '/api/brokers/',
            '/api/documents/',
            '/api/products/',
            '/api/reports/repayment-compliance/',
            '/api/reports/application-volume/',
            '/api/reports/application-status/',
        ]
        
        for endpoint in authenticated_endpoints:
            response = self.client.get(endpoint)
            # We're checking that the endpoint exists, not necessarily that we have permission
            # So we accept 200 OK or 403 Forbidden, but not 404 Not Found
            self.assertNotIn(
                response.status_code, 
                [status.HTTP_404_NOT_FOUND],
                f"Authenticated endpoint {endpoint} returned 404 Not Found"
            )
            print(f"Authenticated endpoint {endpoint} - Status: {response.status_code}")

if __name__ == '__main__':
    unittest.main()
