"""
Tests for asynchronous task views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from applications.models import Application

User = get_user_model()


class TaskViewsTestCase(TestCase):
    """
    Test case for asynchronous task views.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            role='admin'
        )
        
        # Create test application
        self.application = Application.objects.create(
            reference_number='TEST-001',
            application_type='residential',
            purpose='Test purpose',
            loan_amount=100000,
            loan_term=12,
            interest_rate=5.0,
            repayment_frequency='monthly',
            created_by=self.user
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    @patch('crm_backend.task_views.generate_document_async')
    def test_generate_document_async_view(self, mock_task):
        """
        Test generate_document_async_view.
        """
        # Set up mock task
        mock_task.delay.return_value = MagicMock(id='test-task-id', status='PENDING')
        
        # Make request
        url = reverse('generate-document-async', kwargs={'application_id': self.application.id})
        data = {'document_type': 'application_form'}
        response = self.client.post(url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['task_id'], 'test-task-id')
        self.assertEqual(response.data['status'], 'PENDING')
        
        # Check task was called with correct arguments
        mock_task.delay.assert_called_once_with(
            application_id=self.application.id,
            document_type='application_form',
            user_id=self.user.id
        )
    
    @patch('crm_backend.task_views.generate_pdf_async')
    def test_generate_pdf_async_view(self, mock_task):
        """
        Test generate_pdf_async_view.
        """
        # Set up mock task
        mock_task.delay.return_value = MagicMock(id='test-task-id', status='PENDING')
        
        # Make request
        url = reverse('generate-pdf-async', kwargs={'application_id': self.application.id})
        data = {
            'template_name': 'documents/application_form.html',
            'output_filename': 'Test Document',
            'document_type': 'application_form',
            'context': {'test': 'value'}
        }
        response = self.client.post(url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['task_id'], 'test-task-id')
        self.assertEqual(response.data['status'], 'PENDING')
        
        # Check task was called with correct arguments
        mock_task.delay.assert_called_once_with(
            template_name='documents/application_form.html',
            context={'test': 'value'},
            output_filename='Test Document',
            document_type='application_form',
            application_id=self.application.id,
            user_id=self.user.id
        )
    
    @patch('crm_backend.task_views.calculate_funding_async')
    def test_calculate_funding_async_view(self, mock_task):
        """
        Test calculate_funding_async_view.
        """
        # Set up mock task
        mock_task.delay.return_value = MagicMock(id='test-task-id', status='PENDING')
        
        # Make request
        url = reverse('funding-calculation-async', kwargs={'application_id': self.application.id})
        data = {
            'establishment_fee_rate': 1.5,
            'capped_interest_months': 9,
            'monthly_line_fee_rate': 0.5
        }
        response = self.client.post(url, data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['task_id'], 'test-task-id')
        self.assertEqual(response.data['status'], 'PENDING')
        
        # Check task was called with correct arguments
        mock_task.delay.assert_called_once_with(
            application_id=self.application.id,
            calculation_input=data,
            user_id=self.user.id
        )
    
    @patch('crm_backend.task_views.get_task_status')
    def test_task_status_view(self, mock_get_status):
        """
        Test task_status_view.
        """
        # Set up mock status
        mock_get_status.return_value = {
            'task_id': 'test-task-id',
            'status': 'SUCCESS',
            'progress': 100,
            'message': 'Task completed successfully'
        }
        
        # Make request
        url = reverse('task-status', kwargs={'task_id': 'test-task-id'})
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_id'], 'test-task-id')
        self.assertEqual(response.data['status'], 'SUCCESS')
        self.assertEqual(response.data['progress'], 100)
        self.assertEqual(response.data['message'], 'Task completed successfully')
        
        # Check function was called with correct arguments
        mock_get_status.assert_called_once_with('test-task-id')
    
    @patch('crm_backend.task_views.get_task_result')
    def test_task_result_view_success(self, mock_get_result):
        """
        Test task_result_view with successful task.
        """
        # Set up mock result
        mock_get_result.return_value = {
            'task_id': 'test-task-id',
            'status': 'SUCCESS',
            'result': {'document_id': 1}
        }
        
        # Make request
        url = reverse('task-result', kwargs={'task_id': 'test-task-id'})
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['task_id'], 'test-task-id')
        self.assertEqual(response.data['status'], 'SUCCESS')
        self.assertEqual(response.data['result'], {'document_id': 1})
        
        # Check function was called with correct arguments
        mock_get_result.assert_called_once_with('test-task-id')
    
    @patch('crm_backend.task_views.get_task_result')
    def test_task_result_view_pending(self, mock_get_result):
        """
        Test task_result_view with pending task.
        """
        # Set up mock result
        mock_get_result.return_value = {
            'task_id': 'test-task-id',
            'status': 'PENDING',
            'message': 'Task is not yet complete'
        }
        
        # Make request
        url = reverse('task-result', kwargs={'task_id': 'test-task-id'})
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Task is not yet complete')
        self.assertEqual(response.data['status'], 'PENDING')
        
        # Check function was called with correct arguments
        mock_get_result.assert_called_once_with('test-task-id')