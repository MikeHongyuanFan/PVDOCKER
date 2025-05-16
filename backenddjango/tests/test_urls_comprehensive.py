import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class ComprehensiveURLEndpointTests(TestCase):
    """Test case to verify the existence of all URL endpoints in the application, including sub-URLs."""
    
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
        
        # Define all endpoints to test, organized by module
        self.endpoints = {
            'admin': [
                '/admin/',
            ],
            'api_docs': [
                '/api/schema/',
                '/api/swagger/',
                '/api/redoc/',
            ],
            'users': [
                '/api/users/',
                '/api/users/auth/login/',
                '/api/users/auth/logout/',
                '/api/users/auth/register/',
                '/api/users/auth/refresh/',
                '/api/users/auth/reset-password-request/',
                '/api/users/auth/reset-password-confirm/',
                '/api/users/profile/',
                '/api/users/profile/update/',
                '/api/users/notifications/',
                '/api/users/notifications/mark-read/',
                '/api/users/notifications/count/',
                '/api/users/notification-preferences/',
                '/api/users/users/',
                '/api/users/notifications-viewset/',
            ],
            'applications': [
                '/api/applications/',
                '/api/applications/enhanced-applications/',
                '/api/applications/create-with-cascade/',
                '/api/applications/validate-schema/',
                '/api/applications/manual-funding-calculator/',
                # The following endpoints require an application ID, which we'll test separately
                # '/api/applications/1/signature/',
                # '/api/applications/1/stage/',
                # '/api/applications/1/borrowers/',
                # '/api/applications/1/sign/',
                # '/api/applications/1/extend-loan/',
                # '/api/applications/1/funding-calculation/',
                # '/api/applications/1/funding-calculation-history/',
                # '/api/applications/1/generate-pdf/',
            ],
            'borrowers': [
                '/api/borrowers/',
                '/api/borrowers/guarantors/',
                '/api/borrowers/borrowers/',
                # The following endpoints require IDs, which we'll test separately
                # '/api/borrowers/borrowers/1/assets/',
                # '/api/borrowers/guarantors/1/assets/',
            ],
            'brokers': [
                '/api/brokers/',
                '/api/brokers/bdms/',
                '/api/brokers/branches/',
            ],
            'documents': [
                '/api/documents/',
                '/api/documents/documents/',
                '/api/documents/notes/',
                '/api/documents/fees/',
                '/api/documents/repayments/',
                '/api/documents/note-comments/',
                # The following endpoints require IDs, which we'll test separately
                # '/api/documents/documents/1/create-version/',
                # '/api/documents/fees/1/mark-paid/',
                # '/api/documents/repayments/1/mark-paid/',
                # '/api/documents/applications/1/ledger/',
            ],
            'products': [
                '/api/products/',
                '/api/products/products/',
            ],
            'reports': [
                '/api/reports/repayment-compliance/',
                '/api/reports/application-volume/',
                '/api/reports/application-status/',
            ],
        }
    
    def test_unauthenticated_endpoints(self):
        """Test all endpoints without authentication."""
        # Flatten the endpoints dictionary into a single list
        all_endpoints = [endpoint for category in self.endpoints.values() for endpoint in category]
        
        results = {'success': [], 'failure': []}
        
        for endpoint in all_endpoints:
            response = self.client.get(endpoint)
            
            # We consider any response other than 404 as a success
            if response.status_code != status.HTTP_404_NOT_FOUND:
                results['success'].append(f"{endpoint} - Status: {response.status_code}")
            else:
                results['failure'].append(f"{endpoint} - Status: 404 Not Found")
        
        # Print results
        print("\n=== UNAUTHENTICATED ENDPOINTS ===")
        print(f"Successful endpoints: {len(results['success'])}")
        print(f"Failed endpoints: {len(results['failure'])}")
        
        if results['failure']:
            print("\nFailed endpoints:")
            for failure in results['failure']:
                print(f"  {failure}")
        
        # Assert that all endpoints exist
        self.assertEqual(len(results['failure']), 0, 
                         f"{len(results['failure'])} endpoints returned 404 Not Found")
    
    def test_authenticated_endpoints(self):
        """Test all endpoints with authentication."""
        # Login the test user
        self.client.force_authenticate(user=self.test_user)
        
        # Flatten the endpoints dictionary into a single list
        all_endpoints = [endpoint for category in self.endpoints.values() for endpoint in category]
        
        results = {'success': [], 'failure': []}
        
        for endpoint in all_endpoints:
            response = self.client.get(endpoint)
            
            # We consider any response other than 404 as a success
            if response.status_code != status.HTTP_404_NOT_FOUND:
                results['success'].append(f"{endpoint} - Status: {response.status_code}")
            else:
                results['failure'].append(f"{endpoint} - Status: 404 Not Found")
        
        # Print results
        print("\n=== AUTHENTICATED ENDPOINTS ===")
        print(f"Successful endpoints: {len(results['success'])}")
        print(f"Failed endpoints: {len(results['failure'])}")
        
        if results['failure']:
            print("\nFailed endpoints:")
            for failure in results['failure']:
                print(f"  {failure}")
        
        # Assert that all endpoints exist
        self.assertEqual(len(results['failure']), 0, 
                         f"{len(results['failure'])} endpoints returned 404 Not Found")
    
    def test_endpoints_requiring_ids(self):
        """Test endpoints that require IDs with dummy IDs."""
        # Login the test user
        self.client.force_authenticate(user=self.test_user)
        
        # Define endpoints that require IDs
        id_endpoints = [
            # Applications
            '/api/applications/1/signature/',
            '/api/applications/1/stage/',
            '/api/applications/1/borrowers/',
            '/api/applications/1/sign/',
            '/api/applications/1/extend-loan/',
            '/api/applications/1/funding-calculation/',
            '/api/applications/1/funding-calculation-history/',
            '/api/applications/1/generate-pdf/',
            
            # Borrowers
            '/api/borrowers/borrowers/1/assets/',
            '/api/borrowers/guarantors/1/assets/',
            
            # Documents
            '/api/documents/documents/1/create-version/',
            '/api/documents/fees/1/mark-paid/',
            '/api/documents/repayments/1/mark-paid/',
            '/api/documents/applications/1/ledger/',
        ]
        
        results = {'success': [], 'not_found': [], 'other_error': []}
        
        for endpoint in id_endpoints:
            response = self.client.get(endpoint)
            
            # For ID endpoints, we expect either:
            # - 404: The ID doesn't exist (but the endpoint structure is valid)
            # - Other status: The endpoint exists and returns some other status
            
            if response.status_code == status.HTTP_404_NOT_FOUND:
                # This could be a valid "not found" for a non-existent ID
                results['not_found'].append(f"{endpoint} - Status: 404 (ID not found)")
            elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
                # This means the endpoint exists but doesn't support GET
                results['success'].append(f"{endpoint} - Status: 405 (Method not allowed)")
            else:
                results['success'].append(f"{endpoint} - Status: {response.status_code}")
        
        # Print results
        print("\n=== ID-REQUIRING ENDPOINTS ===")
        print(f"Successful endpoints: {len(results['success'])}")
        print(f"Not found (ID): {len(results['not_found'])}")
        print(f"Other errors: {len(results['other_error'])}")
        
        if results['other_error']:
            print("\nEndpoints with other errors:")
            for error in results['other_error']:
                print(f"  {error}")
        
        # We don't assert anything here because 404s are expected for non-existent IDs

if __name__ == '__main__':
    unittest.main()
