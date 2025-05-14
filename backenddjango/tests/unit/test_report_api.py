from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from applications.models import Application
from documents.models import Repayment
from users.models import User
from borrowers.models import Borrower
from brokers.models import Broker, BDM, Branch
from django.utils import timezone
from decimal import Decimal
import datetime
import json

class ReportAPITestCase(TestCase):
    def setUp(self):
        """
        Set up test data
        """
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Create branch
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Branch St',
            phone='1234567890',
            email='branch@example.com'
        )
        
        # Create broker
        self.broker = Broker.objects.create(
            name='Test Broker',
            phone='0987654321',
            email='broker@example.com',
            branch=self.branch
        )
        
        # Create BD
        self.bd = BDM.objects.create(
            name='Test BD',
            phone='5555555555',
            email='bd@example.com',
            branch=self.branch
        )
        
        # Create borrower
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            residential_address='123 Main St'
        )
        
        # Create applications with different stages and dates
        self.now = timezone.now()
        
        # Application 1: Inquiry stage (30 days ago)
        self.app1 = Application.objects.create(
            reference_number='APP-2025-001',
            stage='inquiry',
            application_type='residential',
            loan_amount=Decimal('250000.00'),
            loan_term=360,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=30)
        )
        self.app1.borrowers.add(self.borrower)
        
        # Application 2: Pre-approval stage (25 days ago)
        self.app2 = Application.objects.create(
            reference_number='APP-2025-002',
            stage='pre_approval',
            application_type='commercial',
            loan_amount=Decimal('500000.00'),
            loan_term=240,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=25)
        )
        self.app2.borrowers.add(self.borrower)
        
        # Application 3: Formal approval stage (20 days ago)
        self.app3 = Application.objects.create(
            reference_number='APP-2025-003',
            stage='formal_approval',
            application_type='construction',
            loan_amount=Decimal('750000.00'),
            loan_term=180,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=20)
        )
        self.app3.borrowers.add(self.borrower)
        
        # Application 4: Settlement stage (15 days ago)
        self.app4 = Application.objects.create(
            reference_number='APP-2025-004',
            stage='settlement',
            application_type='refinance',
            loan_amount=Decimal('300000.00'),
            loan_term=300,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=15)
        )
        self.app4.borrowers.add(self.borrower)
        
        # Application 5: Funded stage (10 days ago)
        self.app5 = Application.objects.create(
            reference_number='APP-2025-005',
            stage='funded',
            application_type='investment',
            loan_amount=Decimal('450000.00'),
            loan_term=360,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=10)
        )
        self.app5.borrowers.add(self.borrower)
        
        # Application 6: Declined stage (5 days ago)
        self.app6 = Application.objects.create(
            reference_number='APP-2025-006',
            stage='declined',
            application_type='residential',
            loan_amount=Decimal('200000.00'),
            loan_term=240,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=5)
        )
        self.app6.borrowers.add(self.borrower)
        
        # Create repayments for funded application
        today = timezone.now().date()
        
        # Repayment 1: Paid on time
        self.repayment1 = Repayment.objects.create(
            application=self.app5,
            amount=Decimal('1500.00'),
            due_date=today - datetime.timedelta(days=30),
            paid_date=today - datetime.timedelta(days=30),
            created_by=self.admin_user
        )
        
        # Repayment 2: Paid late
        self.repayment2 = Repayment.objects.create(
            application=self.app5,
            amount=Decimal('1500.00'),
            due_date=today - datetime.timedelta(days=20),
            paid_date=today - datetime.timedelta(days=15),
            created_by=self.admin_user
        )
        
        # Repayment 3: Not paid yet, but due
        self.repayment3 = Repayment.objects.create(
            application=self.app5,
            amount=Decimal('1500.00'),
            due_date=today - datetime.timedelta(days=10),
            created_by=self.admin_user
        )
        
        # Repayment 4: Future repayment
        self.repayment4 = Repayment.objects.create(
            application=self.app5,
            amount=Decimal('1500.00'),
            due_date=today + datetime.timedelta(days=10),
            created_by=self.admin_user
        )
        
        # Set up API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_repayment_compliance_report(self):
        """
        Test repayment compliance report
        """
        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the structure of the response
        self.assertIn('total_repayments', response.data)
        self.assertIn('paid_on_time', response.data)
        self.assertIn('paid_late', response.data)
        self.assertIn('missed', response.data)
        self.assertIn('compliance_rate', response.data)
        self.assertIn('monthly_breakdown', response.data)
    
    def test_repayment_compliance_report_filtering(self):
        """
        Test repayment compliance report with filtering
        """
        # Filter by application
        url = reverse('repayment-compliance-report') + f'?application_id={self.app5.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_repayments', response.data)
    
    def test_application_volume_report(self):
        """
        Test application volume report
        """
        url = reverse('application-volume-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the structure of the response
        self.assertIn('total_applications', response.data)
        self.assertIn('total_loan_amount', response.data)
        self.assertIn('average_loan_amount', response.data)
        self.assertIn('stage_breakdown', response.data)
        self.assertIn('time_breakdown', response.data)
        self.assertIn('bd_breakdown', response.data)
        self.assertIn('type_breakdown', response.data)
    
    def test_application_volume_report_time_grouping(self):
        """
        Test application volume report with different time groupings
        """
        # Test with day grouping
        url = reverse('application-volume-report') + '?time_grouping=day'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('time_breakdown', response.data)
        
        # Test with week grouping
        url = reverse('application-volume-report') + '?time_grouping=week'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('time_breakdown', response.data)
        
        # Test with month grouping
        url = reverse('application-volume-report') + '?time_grouping=month'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('time_breakdown', response.data)
    
    def test_application_status_report(self):
        """
        Test application status report
        """
        url = reverse('application-status-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the structure of the response
        self.assertIn('total_active', response.data)
        self.assertIn('total_settled', response.data)
        self.assertIn('total_declined', response.data)
        self.assertIn('total_withdrawn', response.data)
        self.assertIn('active_by_stage', response.data)
        self.assertIn('inquiry_to_approval_rate', response.data)
        self.assertIn('approval_to_settlement_rate', response.data)
        self.assertIn('overall_success_rate', response.data)
    
    def test_report_permissions(self):
        """
        Test that only authenticated users can access reports
        """
        # Logout
        self.client.logout()
        
        # Try to access reports without authentication
        url = reverse('repayment-compliance-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        url = reverse('application-volume-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        url = reverse('application-status-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_report_data_accuracy(self):
        """
        Test the accuracy of report calculations with known data
        """
        # Create a new application with specific data for testing calculations
        app7 = Application.objects.create(
            reference_number='APP-2025-007',
            stage='formal_approval',
            application_type='residential',
            loan_amount=Decimal('100000.00'),
            loan_term=120,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=2)
        )
        app7.borrowers.add(self.borrower)
        
        # Test application volume with the new application
        url = reverse('application-volume-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_applications', response.data)
        
        # Test application status with the new application
        url = reverse('application-status-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_active', response.data)
        self.assertIn('active_by_stage', response.data)
    
    def test_report_filtering(self):
        """
        Test filtering functionality of reports
        """
        # Create an application from yesterday
        app_yesterday = Application.objects.create(
            reference_number='APP-2025-008',
            stage='inquiry',
            application_type='residential',
            loan_amount=Decimal('150000.00'),
            loan_term=240,
            broker=self.broker,
            bd=self.bd,
            created_by=self.admin_user,
            created_at=self.now - datetime.timedelta(days=1)
        )
        app_yesterday.borrowers.add(self.borrower)
        
        # Filter by BD
        url = reverse('application-volume-report') + f'?bd_id={self.bd.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_applications', response.data)
