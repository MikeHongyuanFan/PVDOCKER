"""
Test admin user API access.
Verifies that admin users have access to all API endpoints.
"""

from django.urls import reverse
from rest_framework import status
from .base import AdminIntegrationTestCase


class AdminAPIAccessTest(AdminIntegrationTestCase):
    """
    Test that admin users have access to all API endpoints.
    """
    
    def test_admin_user_profile_access(self):
        """
        Test that admin users can access their own profile.
        """
        url = reverse('user-detail', args=[self.admin_user.id])
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assert_response_contains(response, 'email', self.admin_user.email)
    
    def test_admin_users_list_access(self):
        """
        Test that admin users can access the users list.
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_applications_access(self):
        """
        Test that admin users can access applications.
        """
        url = reverse('application-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_borrowers_access(self):
        """
        Test that admin users can access borrowers.
        """
        url = reverse('borrower-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_documents_access(self):
        """
        Test that admin users can access documents.
        """
        url = reverse('document-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_reports_access(self):
        """
        Test that admin users can access reports.
        """
        # Test application volume report
        url = reverse('application-volume-report')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        
        # Test application status report
        url = reverse('application-status-report')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        
        # Test repayment compliance report
        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
    
    def test_admin_notifications_access(self):
        """
        Test that admin users can access notifications.
        """
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_brokers_access(self):
        """
        Test that admin users can access brokers.
        """
        url = reverse('broker-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_bdm_access(self):
        """
        Test that admin users can access BDMs.
        """
        url = reverse('bdm-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_admin_branches_access(self):
        """
        Test that admin users can access branches.
        """
        url = reverse('branch-list')
        response = self.client.get(url)
        self.assert_status_code(response, status.HTTP_200_OK)
        self.assertIn('results', response.data)
