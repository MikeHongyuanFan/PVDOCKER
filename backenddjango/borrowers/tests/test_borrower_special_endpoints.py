"""
Integration tests for special endpoints of the Borrower API.

This test suite covers special endpoints like financial summary and company borrower endpoints,
with different user roles (admin, broker, bd, client) and various test scenarios.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from borrowers.models import Borrower, Asset, Liability
from users.models import User
from tests.integration.factories.user_factory import (
    AdminUserFactory, BrokerUserFactory, UserFactory, ClientUserFactory
)
from tests.integration.factories.borrower_factory import BorrowerFactory, CompanyBorrowerFactory
import json
from decimal import Decimal


class BorrowerSpecialEndpointsTestBase(APITestCase):
    """Base test class for Borrower special endpoints tests."""
    
    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = AdminUserFactory()
        self.broker_user = BrokerUserFactory()
        self.bd_user = UserFactory(role='bd', username='bd_user', email='bd@example.com')
        self.client_user = ClientUserFactory()
        
        # Create borrowers
        self.admin_borrower = BorrowerFactory(
            first_name="Admin",
            last_name="Borrower",
            email="admin.borrower@example.com",
            created_by=self.admin_user,
            annual_income=Decimal('120000.00'),
            other_income=Decimal('10000.00'),
            monthly_expenses=Decimal('3000.00')
        )
        
        self.broker_borrower = BorrowerFactory(
            first_name="Broker",
            last_name="Borrower",
            email="broker.borrower@example.com",
            created_by=self.broker_user,
            annual_income=Decimal('80000.00'),
            other_income=Decimal('5000.00'),
            monthly_expenses=Decimal('2000.00')
        )
        
        self.client_borrower = BorrowerFactory(
            first_name="Client",
            last_name="Borrower",
            email="client.borrower@example.com",
            created_by=self.admin_user,
            user=self.client_user,
            annual_income=Decimal('60000.00'),
            monthly_expenses=Decimal('1500.00')
        )
        
        # Create company borrowers
        self.admin_company = CompanyBorrowerFactory(
            company_name="Admin Company",
            email="admin.company@example.com",
            created_by=self.admin_user,
            annual_company_income=Decimal('500000.00')
        )
        
        self.broker_company = CompanyBorrowerFactory(
            company_name="Broker Company",
            email="broker.company@example.com",
            created_by=self.broker_user,
            annual_company_income=Decimal('300000.00')
        )
        
        # Create assets and liabilities for financial summary testing
        # Admin borrower assets
        self.admin_asset1 = Asset.objects.create(
            borrower=self.admin_borrower,
            asset_type='property',
            description='Primary residence',
            value=Decimal('500000.00'),
            created_by=self.admin_user
        )
        
        self.admin_asset2 = Asset.objects.create(
            borrower=self.admin_borrower,
            asset_type='vehicle',
            description='Car',
            value=Decimal('30000.00'),
            created_by=self.admin_user
        )
        
        # Admin borrower liabilities
        self.admin_liability1 = Liability.objects.create(
            borrower=self.admin_borrower,
            liability_type='mortgage',
            description='Home loan',
            amount=Decimal('300000.00'),
            monthly_payment=Decimal('1500.00'),
            created_by=self.admin_user
        )
        
        self.admin_liability2 = Liability.objects.create(
            borrower=self.admin_borrower,
            liability_type='car_loan',
            description='Car loan',
            amount=Decimal('20000.00'),
            monthly_payment=Decimal('400.00'),
            created_by=self.admin_user
        )
        
        # Broker borrower assets
        self.broker_asset = Asset.objects.create(
            borrower=self.broker_borrower,
            asset_type='savings',
            description='Savings account',
            value=Decimal('50000.00'),
            created_by=self.broker_user
        )
        
        # Broker borrower liabilities
        self.broker_liability = Liability.objects.create(
            borrower=self.broker_borrower,
            liability_type='credit_card',
            description='Credit card debt',
            amount=Decimal('5000.00'),
            monthly_payment=Decimal('200.00'),
            created_by=self.broker_user
        )
        
        # Set up API client
        self.client = APIClient()
        
    def get_borrower_financial_summary_url(self, borrower_id):
        """Get URL for borrower financial summary endpoint."""
        return reverse('borrower-financial-summary', kwargs={'pk': borrower_id})
    
    def get_company_borrower_list_url(self):
        """Get URL for company borrower list endpoint."""
        return reverse('company-borrower-list')


class TestFinancialSummaryEndpoint(BorrowerSpecialEndpointsTestBase):
    """Test cases for the financial summary endpoint."""
    
    def test_financial_summary_admin(self):
        """Test that admin can get financial summary for any borrower."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Admin can get financial summary for admin borrower
        url = self.get_borrower_financial_summary_url(self.admin_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the summary contains the expected fields
        self.assertIn('total_assets', response.data)
        self.assertIn('total_liabilities', response.data)
        self.assertIn('net_worth', response.data)
        self.assertIn('monthly_income', response.data)
        self.assertIn('monthly_expenses', response.data)
        self.assertIn('disposable_income', response.data)
        self.assertIn('asset_breakdown', response.data)
        self.assertIn('liability_breakdown', response.data)
        
        # Check that the calculations are correct
        expected_total_assets = self.admin_asset1.value + self.admin_asset2.value
        expected_total_liabilities = self.admin_liability1.amount + self.admin_liability2.amount
        expected_net_worth = expected_total_assets - expected_total_liabilities
        expected_monthly_income = (self.admin_borrower.annual_income / 12) + self.admin_borrower.other_income
        expected_monthly_expenses = self.admin_borrower.monthly_expenses + self.admin_liability1.monthly_payment + self.admin_liability2.monthly_payment
        expected_disposable_income = expected_monthly_income - expected_monthly_expenses
        
        self.assertEqual(Decimal(response.data['total_assets']), expected_total_assets)
        self.assertEqual(Decimal(response.data['total_liabilities']), expected_total_liabilities)
        self.assertEqual(Decimal(response.data['net_worth']), expected_net_worth)
        self.assertEqual(Decimal(response.data['monthly_income']), expected_monthly_income)
        self.assertEqual(Decimal(response.data['monthly_expenses']), expected_monthly_expenses)
        self.assertEqual(Decimal(response.data['disposable_income']), expected_disposable_income)
        
        # Admin can get financial summary for broker borrower
        url = self.get_borrower_financial_summary_url(self.broker_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_financial_summary_broker(self):
        """Test that broker can only get financial summary for their own borrowers."""
        self.client.force_authenticate(user=self.broker_user)
        
        # Broker can get financial summary for their own borrower
        url = self.get_borrower_financial_summary_url(self.broker_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the calculations are correct
        expected_total_assets = self.broker_asset.value
        expected_total_liabilities = self.broker_liability.amount
        expected_net_worth = expected_total_assets - expected_total_liabilities
        expected_monthly_income = (self.broker_borrower.annual_income / 12) + self.broker_borrower.other_income
        expected_monthly_expenses = self.broker_borrower.monthly_expenses + self.broker_liability.monthly_payment
        expected_disposable_income = expected_monthly_income - expected_monthly_expenses
        
        self.assertEqual(Decimal(response.data['total_assets']), expected_total_assets)
        self.assertEqual(Decimal(response.data['total_liabilities']), expected_total_liabilities)
        self.assertEqual(Decimal(response.data['net_worth']), expected_net_worth)
        self.assertEqual(Decimal(response.data['monthly_income']), expected_monthly_income)
        self.assertEqual(Decimal(response.data['monthly_expenses']), expected_monthly_expenses)
        self.assertEqual(Decimal(response.data['disposable_income']), expected_disposable_income)
        
        # Broker cannot get financial summary for admin borrower
        url = self.get_borrower_financial_summary_url(self.admin_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_financial_summary_bd(self):
        """Test that BD can get financial summary for borrowers."""
        self.client.force_authenticate(user=self.bd_user)
        
        # Create a borrower for BD
        bd_borrower = BorrowerFactory(
            first_name="BD",
            last_name="Borrower",
            email="bd.borrower@example.com",
            created_by=self.bd_user,
            annual_income=Decimal('90000.00'),
            monthly_expenses=Decimal('2500.00')
        )
        
        # Create asset and liability for BD borrower
        bd_asset = Asset.objects.create(
            borrower=bd_borrower,
            asset_type='property',
            description='Investment property',
            value=Decimal('400000.00'),
            created_by=self.bd_user
        )
        
        bd_liability = Liability.objects.create(
            borrower=bd_borrower,
            liability_type='mortgage',
            description='Investment loan',
            amount=Decimal('250000.00'),
            monthly_payment=Decimal('1200.00'),
            created_by=self.bd_user
        )
        
        # BD can get financial summary for their own borrower
        url = self.get_borrower_financial_summary_url(bd_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # BD cannot get financial summary for admin borrower
        url = self.get_borrower_financial_summary_url(self.admin_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_financial_summary_client(self):
        """Test that client can only get financial summary for their own borrower profile."""
        self.client.force_authenticate(user=self.client_user)
        
        # Create asset and liability for client borrower
        client_asset = Asset.objects.create(
            borrower=self.client_borrower,
            asset_type='savings',
            description='Savings account',
            value=Decimal('20000.00'),
            created_by=self.admin_user
        )
        
        client_liability = Liability.objects.create(
            borrower=self.client_borrower,
            liability_type='personal_loan',
            description='Personal loan',
            amount=Decimal('10000.00'),
            monthly_payment=Decimal('300.00'),
            created_by=self.admin_user
        )
        
        # Client can get financial summary for their own borrower profile
        url = self.get_borrower_financial_summary_url(self.client_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Client cannot get financial summary for admin borrower
        url = self.get_borrower_financial_summary_url(self.admin_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_financial_summary_nonexistent_borrower(self):
        """Test getting financial summary for a nonexistent borrower."""
        self.client.force_authenticate(user=self.admin_user)
        
        url = self.get_borrower_financial_summary_url(999999)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_financial_summary_unauthorized(self):
        """Test unauthorized access to financial summary endpoint."""
        # No authentication
        url = self.get_borrower_financial_summary_url(self.admin_borrower.id)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCompanyBorrowerEndpoint(BorrowerSpecialEndpointsTestBase):
    """Test cases for the company borrower endpoint."""
    
    def test_company_borrower_list_admin(self):
        """Test that admin can list all company borrowers."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(self.get_company_borrower_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all company borrowers
        company_names = [item['company_name'] for item in response.data]
        self.assertIn(self.admin_company.company_name, company_names)
        self.assertIn(self.broker_company.company_name, company_names)
        self.assertEqual(len(response.data), 2)
    
    def test_company_borrower_list_broker(self):
        """Test that broker can only list company borrowers they created or have access to."""
        self.client.force_authenticate(user=self.broker_user)
        
        response = self.client.get(self.get_company_borrower_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Broker should only see company borrowers they created or have access to
        company_names = [item['company_name'] for item in response.data]
        self.assertIn(self.broker_company.company_name, company_names)
        self.assertNotIn(self.admin_company.company_name, company_names)
        self.assertEqual(len(response.data), 1)
    
    def test_company_borrower_list_bd(self):
        """Test that BD can list company borrowers they created or have access to."""
        self.client.force_authenticate(user=self.bd_user)
        
        # Create a company borrower for BD
        bd_company = CompanyBorrowerFactory(
            company_name="BD Company",
            email="bd.company@example.com",
            created_by=self.bd_user,
            annual_company_income=Decimal('400000.00')
        )
        
        response = self.client.get(self.get_company_borrower_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # BD should only see company borrowers they created or have access to
        company_names = [item['company_name'] for item in response.data]
        self.assertIn(bd_company.company_name, company_names)
        self.assertNotIn(self.admin_company.company_name, company_names)
        self.assertEqual(len(response.data), 1)
    
    def test_company_borrower_list_client(self):
        """Test that client cannot access company borrower list."""
        self.client.force_authenticate(user=self.client_user)
        
        response = self.client.get(self.get_company_borrower_list_url())
        
        # Client should not have permission to access company borrower list
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_company_borrower_list_unauthorized(self):
        """Test unauthorized access to company borrower list endpoint."""
        # No authentication
        response = self.client.get(self.get_company_borrower_list_url())
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_company_borrower(self):
        """Test creating a company borrower."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'is_company': True,
            'company_name': 'New Test Company',
            'company_abn': '12345678901',
            'company_acn': '123456789',
            'email': 'new.company@example.com',
            'industry_type': 'finance',
            'contact_number': '0412345678',
            'annual_company_income': '600000.00',
            'registered_address_street_no': '123',
            'registered_address_street_name': 'Main Street',
            'registered_address_suburb': 'Sydney',
            'registered_address_state': 'NSW',
            'registered_address_postcode': '2000'
        }
        
        response = self.client.post(reverse('borrower-list'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['company_name'], data['company_name'])
        self.assertTrue(response.data['is_company'])
        
        # Verify company borrower was created in database
        self.assertTrue(Borrower.objects.filter(company_name=data['company_name']).exists())
        
        # Verify the company appears in the company borrower list
        response = self.client.get(self.get_company_borrower_list_url())
        company_names = [item['company_name'] for item in response.data]
        self.assertIn(data['company_name'], company_names)
    
    def test_update_company_borrower(self):
        """Test updating a company borrower."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'company_name': 'Updated Company Name',
            'annual_company_income': '700000.00'
        }
        
        response = self.client.patch(reverse('borrower-detail', kwargs={'pk': self.admin_company.id}), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], data['company_name'])
        self.assertEqual(response.data['annual_company_income'], data['annual_company_income'])
        
        # Verify company borrower was updated in database
        self.admin_company.refresh_from_db()
        self.assertEqual(self.admin_company.company_name, data['company_name'])
        self.assertEqual(str(self.admin_company.annual_company_income), data['annual_company_income'])