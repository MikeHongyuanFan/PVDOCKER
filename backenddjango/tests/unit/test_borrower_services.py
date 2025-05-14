"""
Unit tests for borrower services.
"""

import pytest
from decimal import Decimal
from borrowers.services import (
    create_borrower_with_financials,
    create_guarantor_for_application,
    get_borrower_financial_summary
)
from borrowers.models import Borrower, Guarantor, Asset, Liability
from applications.models import Application


@pytest.mark.django_db
class TestBorrowerCreationService:
    """Test the borrower creation service."""
    
    def test_create_borrower_with_financials(self, staff_user):
        """Test creating a borrower with financial information."""
        # Prepare test data
        borrower_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'residential_address': '123 Main St',
            'date_of_birth': '1980-01-01',
            'employment_type': 'full_time',
            'annual_income': Decimal('75000.00')
        }
        
        assets_data = [
            {
                'asset_type': 'property',
                'description': 'Primary Residence',
                'value': Decimal('500000.00'),
                'address': '123 Main St'
            },
            {
                'asset_type': 'vehicle',
                'description': 'Car',
                'value': Decimal('25000.00')
            }
        ]
        
        liabilities_data = [
            {
                'liability_type': 'mortgage',
                'description': 'Home Loan',
                'amount': Decimal('400000.00'),
                'lender': 'Example Bank',
                'monthly_payment': Decimal('2000.00')
            },
            {
                'liability_type': 'car_loan',
                'description': 'Car Loan',
                'amount': Decimal('15000.00'),
                'lender': 'Auto Finance',
                'monthly_payment': Decimal('500.00')
            }
        ]
        
        # Create borrower with financials
        borrower = create_borrower_with_financials(
            borrower_data=borrower_data,
            assets_data=assets_data,
            liabilities_data=liabilities_data,
            user=staff_user
        )
        
        # Verify borrower was created
        assert borrower is not None
        assert borrower.first_name == 'John'
        assert borrower.last_name == 'Doe'
        assert borrower.email == 'john.doe@example.com'
        assert borrower.created_by == staff_user
        
        # Verify assets were created
        assets = borrower.assets.all()
        assert assets.count() == 2
        
        property_asset = assets.filter(asset_type='property').first()
        assert property_asset is not None
        assert property_asset.value == Decimal('500000.00')
        assert property_asset.description == 'Primary Residence'
        assert property_asset.created_by == staff_user
        
        vehicle_asset = assets.filter(asset_type='vehicle').first()
        assert vehicle_asset is not None
        assert vehicle_asset.value == Decimal('25000.00')
        
        # Verify liabilities were created
        liabilities = borrower.liabilities.all()
        assert liabilities.count() == 2
        
        mortgage = liabilities.filter(liability_type='mortgage').first()
        assert mortgage is not None
        assert mortgage.amount == Decimal('400000.00')
        assert mortgage.monthly_payment == Decimal('2000.00')
        assert mortgage.created_by == staff_user
        
        car_loan = liabilities.filter(liability_type='car_loan').first()
        assert car_loan is not None
        assert car_loan.amount == Decimal('15000.00')
    
    def test_create_borrower_without_financials(self, staff_user):
        """Test creating a borrower without financial information."""
        # Prepare test data
        borrower_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '9876543210',
            'residential_address': '456 Oak St',
            'date_of_birth': '1985-05-15',
            'employment_type': 'self_employed',
            'annual_income': Decimal('120000.00')
        }
        
        # Create borrower without financials
        borrower = create_borrower_with_financials(
            borrower_data=borrower_data,
            user=staff_user
        )
        
        # Verify borrower was created
        assert borrower is not None
        assert borrower.first_name == 'Jane'
        assert borrower.last_name == 'Smith'
        assert borrower.email == 'jane.smith@example.com'
        assert borrower.created_by == staff_user
        
        # Verify no assets or liabilities were created
        assert borrower.assets.count() == 0
        assert borrower.liabilities.count() == 0
    
    def test_create_company_borrower(self, staff_user):
        """Test creating a company borrower."""
        # Prepare test data
        company_data = {
            'is_company': True,
            'company_name': 'Test Company Ltd',
            'company_abn': '12345678901',
            'company_acn': '123456789',
            'company_address': '789 Business Ave',
            'email': 'info@testcompany.com',
            'phone': '5551234567'
        }
        
        # Create company borrower
        company = create_borrower_with_financials(
            borrower_data=company_data,
            user=staff_user
        )
        
        # Verify company was created
        assert company is not None
        assert company.is_company is True
        assert company.company_name == 'Test Company Ltd'
        assert company.company_abn == '12345678901'
        assert company.created_by == staff_user


@pytest.mark.django_db
class TestGuarantorCreationService:
    """Test the guarantor creation service."""
    
    def test_create_guarantor_for_application(self, staff_user, individual_borrower):
        """Test creating a guarantor for an application."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(individual_borrower)
        
        # Prepare guarantor data
        guarantor_data = {
            'guarantor_type': 'individual',
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'date_of_birth': '1975-03-20',
            'email': 'michael.johnson@example.com',
            'phone': '5551234567',
            'address': '789 Guarantor St'
        }
        
        # Create guarantor
        guarantor = create_guarantor_for_application(
            guarantor_data=guarantor_data,
            borrower_id=individual_borrower.id,
            application_id=application.id,
            user=staff_user
        )
        
        # Verify guarantor was created
        assert guarantor is not None
        assert guarantor.guarantor_type == 'individual'
        assert guarantor.first_name == 'Michael'
        assert guarantor.last_name == 'Johnson'
        assert guarantor.borrower == individual_borrower
        assert guarantor.application == application
        assert guarantor.created_by == staff_user
    
    def test_create_company_guarantor(self, staff_user, individual_borrower):
        """Test creating a company guarantor."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-002",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(individual_borrower)
        
        # Prepare company guarantor data
        guarantor_data = {
            'guarantor_type': 'company',
            'company_name': 'Guarantor Company Ltd',
            'company_abn': '98765432109',
            'company_acn': '987654321',
            'email': 'info@guarantorcompany.com',
            'phone': '5559876543',
            'address': '101 Corporate Blvd'
        }
        
        # Create guarantor
        guarantor = create_guarantor_for_application(
            guarantor_data=guarantor_data,
            borrower_id=individual_borrower.id,
            application_id=application.id,
            user=staff_user
        )
        
        # Verify guarantor was created
        assert guarantor is not None
        assert guarantor.guarantor_type == 'company'
        assert guarantor.company_name == 'Guarantor Company Ltd'
        assert guarantor.company_abn == '98765432109'
        assert guarantor.borrower == individual_borrower
        assert guarantor.application == application
    
    def test_create_guarantor_invalid_borrower(self, staff_user):
        """Test creating a guarantor with an invalid borrower ID."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-003",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Prepare guarantor data
        guarantor_data = {
            'guarantor_type': 'individual',
            'first_name': 'Invalid',
            'last_name': 'Guarantor',
            'email': 'invalid@example.com'
        }
        
        # Try to create guarantor with invalid borrower ID
        guarantor = create_guarantor_for_application(
            guarantor_data=guarantor_data,
            borrower_id=999999,  # Invalid ID
            application_id=application.id,
            user=staff_user
        )
        
        # Verify guarantor was not created
        assert guarantor is None
    
    def test_create_guarantor_invalid_application(self, staff_user, individual_borrower):
        """Test creating a guarantor with an invalid application ID."""
        # Prepare guarantor data
        guarantor_data = {
            'guarantor_type': 'individual',
            'first_name': 'Invalid',
            'last_name': 'Guarantor',
            'email': 'invalid@example.com'
        }
        
        # Try to create guarantor with invalid application ID
        guarantor = create_guarantor_for_application(
            guarantor_data=guarantor_data,
            borrower_id=individual_borrower.id,
            application_id=999999,  # Invalid ID
            user=staff_user
        )
        
        # Verify guarantor was not created
        assert guarantor is None


@pytest.mark.django_db
class TestBorrowerFinancialSummaryService:
    """Test the borrower financial summary service."""
    
    def test_get_borrower_financial_summary(self, staff_user):
        """Test getting a financial summary for a borrower."""
        # Create a borrower with financial information
        borrower = Borrower.objects.create(
            first_name='Financial',
            last_name='Test',
            email='financial.test@example.com',
            annual_income=Decimal('120000.00'),
            other_income=Decimal('12000.00'),
            monthly_expenses=Decimal('3000.00'),
            created_by=staff_user
        )
        
        # Create assets
        Asset.objects.create(
            borrower=borrower,
            asset_type='property',
            description='Primary Residence',
            value=Decimal('750000.00'),
            created_by=staff_user
        )
        
        Asset.objects.create(
            borrower=borrower,
            asset_type='savings',
            description='Savings Account',
            value=Decimal('50000.00'),
            created_by=staff_user
        )
        
        # Create liabilities
        Liability.objects.create(
            borrower=borrower,
            liability_type='mortgage',
            description='Home Loan',
            amount=Decimal('500000.00'),
            monthly_payment=Decimal('2500.00'),
            created_by=staff_user
        )
        
        Liability.objects.create(
            borrower=borrower,
            liability_type='credit_card',
            description='Credit Card',
            amount=Decimal('10000.00'),
            monthly_payment=Decimal('500.00'),
            created_by=staff_user
        )
        
        # Get financial summary
        summary = get_borrower_financial_summary(borrower.id)
        
        # Verify summary data
        assert summary is not None
        assert summary['total_assets'] == Decimal('800000.00')  # 750000 + 50000
        assert summary['total_liabilities'] == Decimal('510000.00')  # 500000 + 10000
        assert summary['net_worth'] == Decimal('290000.00')  # 800000 - 510000
        
        # Verify income calculations
        assert summary['monthly_income'] == Decimal('22000.00')  # (120000 / 12) + 12000
        assert summary['monthly_expenses'] == Decimal('6000.00')  # 3000 + 2500 + 500
        assert summary['disposable_income'] == Decimal('16000.00')  # 22000 - 6000
        
        # Verify breakdowns
        assert len(summary['asset_breakdown']) == 2
        assert len(summary['liability_breakdown']) == 2
    
    def test_get_borrower_financial_summary_no_financials(self, staff_user):
        """Test getting a financial summary for a borrower with no financial information."""
        # Create a borrower with no financial information
        borrower = Borrower.objects.create(
            first_name='No',
            last_name='Financials',
            email='no.financials@example.com',
            created_by=staff_user
        )
        
        # Get financial summary
        summary = get_borrower_financial_summary(borrower.id)
        
        # Verify summary data
        assert summary is not None
        assert summary['total_assets'] == 0
        assert summary['total_liabilities'] == 0
        assert summary['net_worth'] == 0
        assert summary['monthly_income'] == 0
        assert summary['monthly_expenses'] == 0
        assert summary['disposable_income'] == 0
        assert len(summary['asset_breakdown']) == 0
        assert len(summary['liability_breakdown']) == 0
    
    def test_get_borrower_financial_summary_invalid_id(self):
        """Test getting a financial summary for a non-existent borrower."""
        summary = get_borrower_financial_summary(999999)
        assert summary is None
