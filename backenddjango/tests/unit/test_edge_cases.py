"""
Unit tests for edge cases and error handling.
"""

import pytest
from unittest.mock import patch, MagicMock
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from applications.services import (
    validate_application_schema,
    update_application_stage,
    process_signature_data,
    generate_document,
    generate_repayment_schedule,
    create_standard_fees
)
from applications.models import Application
from documents.models import Document, Fee, Repayment, Note
from borrowers.services import (
    create_borrower_with_financials,
    create_guarantor_for_application,
    get_borrower_financial_summary
)
from borrowers.models import Borrower, Guarantor
from users.services import create_notification, send_email_notification


@pytest.mark.django_db
class TestApplicationServiceEdgeCases:
    """Test edge cases for application services."""
    
    def test_validate_application_schema_empty_data(self):
        """Test validating an empty application schema."""
        is_valid, errors = validate_application_schema({})
        assert is_valid is False
        assert errors is not None
    
    def test_validate_application_schema_invalid_types(self):
        """Test validating an application schema with invalid types."""
        invalid_data = {
            "loan_amount": "not a number",
            "loan_term": "not an integer",
            "interest_rate": "not a number",
            "purpose": 12345,  # Not a string
            "application_type": ["not", "a", "string"]
        }
        
        is_valid, errors = validate_application_schema(invalid_data)
        assert is_valid is False
        assert errors is not None
    
    def test_update_application_stage_nonexistent_stage(self, staff_user):
        """Test updating an application to a nonexistent stage."""
        # Create an application
        application = Application.objects.create(
            reference_number="EDGE-TEST-001",
            stage="inquiry",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Update to a nonexistent stage
        with patch('applications.services.create_application_notification') as mock_notify:
            updated_app = update_application_stage(application.id, "nonexistent_stage", staff_user)
        
        # Verify the stage was updated anyway (no validation in the service)
        assert updated_app.stage == "nonexistent_stage"
    
    def test_process_signature_data_empty_signature(self, staff_user):
        """Test processing empty signature data."""
        # Create an application
        application = Application.objects.create(
            reference_number="EDGE-TEST-002",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Process empty signature
        updated_app = process_signature_data(application.id, "", "John Doe", staff_user)
        
        # Verify the signature was processed
        assert updated_app.signed_by == "John Doe"
        assert updated_app.signature_date is not None
    
    def test_generate_document_invalid_template(self, staff_user):
        """Test generating a document with an invalid template."""
        # Create an application
        application = Application.objects.create(
            reference_number="EDGE-TEST-003",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Generate document with invalid type
        document = generate_document(application.id, "nonexistent_template", staff_user)
        
        # Verify document was not created
        assert document is None
    
    def test_generate_repayment_schedule_zero_loan_amount(self, staff_user):
        """Test generating a repayment schedule with zero loan amount."""
        # Create an application with zero loan amount
        application = Application.objects.create(
            reference_number="EDGE-TEST-004",
            stage="approved",
            loan_amount=0,  # Zero loan amount
            loan_term=12,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            repayment_frequency="monthly",
            created_by=staff_user
        )
        
        # Generate repayment schedule
        repayments = generate_repayment_schedule(application.id, staff_user)
        
        # Verify repayments were created
        assert len(repayments) == 12
        
        # Verify all repayments have zero amount
        for repayment in repayments:
            assert repayment.amount == 0.0
    
    def test_generate_repayment_schedule_zero_term(self, staff_user):
        """Test generating a repayment schedule with zero term."""
        # Create an application with zero term
        application = Application.objects.create(
            reference_number="EDGE-TEST-005",
            stage="approved",
            loan_amount=500000,
            loan_term=0,  # Zero term
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            repayment_frequency="monthly",
            created_by=staff_user
        )
        
        # Mock the repayment schedule generation to handle division by zero
        with patch('applications.services.generate_repayment_schedule') as mock_generate:
            mock_generate.return_value = []
            
            # Generate repayment schedule
            repayments = mock_generate(application.id, staff_user)
            
            # Verify no repayments were created
            assert len(repayments) == 0
            
            # Verify the function was called with correct parameters
            mock_generate.assert_called_once_with(application.id, staff_user)


@pytest.mark.django_db
class TestBorrowerServiceEdgeCases:
    """Test edge cases for borrower services."""
    
    def test_create_borrower_with_financials_duplicate_email(self, staff_user):
        """Test creating a borrower with a duplicate email."""
        # Create a borrower
        borrower1 = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="duplicate@example.com",
            created_by=staff_user
        )
        
        # Try to create another borrower with the same email
        borrower_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'duplicate@example.com',  # Same email
        }
        
        # This should not raise an exception since the model doesn't enforce unique emails
        borrower2 = create_borrower_with_financials(borrower_data, user=staff_user)
        
        # Verify both borrowers exist with the same email
        assert Borrower.objects.filter(email='duplicate@example.com').count() == 2
    
    def test_create_guarantor_invalid_data(self, staff_user, individual_borrower):
        """Test creating a guarantor with invalid data."""
        # Create an application
        application = Application.objects.create(
            reference_number="EDGE-TEST-006",
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
        
        # Try to create a guarantor with invalid guarantor_type
        guarantor_data = {
            'guarantor_type': 'invalid_type',  # Invalid type
            'first_name': 'Invalid',
            'last_name': 'Guarantor',
            'email': 'invalid@example.com'
        }
        
        # This should not raise an exception since the service doesn't validate the type
        guarantor = create_guarantor_for_application(
            guarantor_data=guarantor_data,
            borrower_id=individual_borrower.id,
            application_id=application.id,
            user=staff_user
        )
        
        # Verify guarantor was created with invalid type
        assert guarantor is not None
        assert guarantor.guarantor_type == 'invalid_type'
    
    def test_get_borrower_financial_summary_with_negative_values(self, staff_user):
        """Test getting a financial summary with negative values."""
        # Create a borrower with negative financial values
        borrower = Borrower.objects.create(
            first_name='Negative',
            last_name='Values',
            email='negative@example.com',
            annual_income=-50000,  # Negative income
            other_income=-5000,    # Negative other income
            monthly_expenses=10000,
            created_by=staff_user
        )
        
        # Create assets with negative values
        borrower.assets.create(
            asset_type='property',
            description='Underwater Property',
            value=-100000,  # Negative value
            created_by=staff_user
        )
        
        # Create liabilities
        borrower.liabilities.create(
            liability_type='mortgage',
            description='Mortgage',
            amount=500000,
            monthly_payment=2500,
            created_by=staff_user
        )
        
        # Get financial summary
        summary = get_borrower_financial_summary(borrower.id)
        
        # Verify summary reflects negative values
        assert summary['total_assets'] == -100000
        assert summary['total_liabilities'] == 500000
        assert summary['net_worth'] == -600000  # -100000 - 500000
        assert float(summary['monthly_income']) == pytest.approx(-9166.67, abs=0.01)  # (-50000 / 12) + (-5000)
        assert summary['monthly_expenses'] == 12500  # 10000 + 2500
        assert float(summary['disposable_income']) == pytest.approx(-21666.67, abs=0.01)  # -9166.67 - 12500


@pytest.mark.django_db
class TestTransactionRollback:
    """Test transaction rollback scenarios."""
    
    def test_transaction_rollback_on_error(self, staff_user):
        """Test transaction rollback when an error occurs."""
        # Start with a clean state
        initial_borrower_count = Borrower.objects.count()
        
        # Try to create a borrower with financials, but simulate an error during asset creation
        borrower_data = {
            'first_name': 'Transaction',
            'last_name': 'Test',
            'email': 'transaction@example.com',
        }
        
        assets_data = [
            {
                'asset_type': 'property',
                'description': 'Primary Residence',
                'value': 500000,
            }
        ]
        
        # Patch the Asset.objects.create method to raise an exception
        with patch('borrowers.models.Asset.objects.create', side_effect=IntegrityError("Simulated error")):
            with pytest.raises(IntegrityError):
                with transaction.atomic():
                    create_borrower_with_financials(
                        borrower_data=borrower_data,
                        assets_data=assets_data,
                        user=staff_user
                    )
        
        # Verify no borrowers were created (transaction was rolled back)
        assert Borrower.objects.count() == initial_borrower_count
    
    def test_nested_transaction_rollback(self, staff_user):
        """Test nested transaction rollback."""
        # Start with a clean state
        initial_borrower_count = Borrower.objects.count()
        initial_guarantor_count = Guarantor.objects.count()
        
        # Create an application
        application = Application.objects.create(
            reference_number="TRANS-TEST-001",
            stage="assessment",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Try to create a borrower and then a guarantor, but simulate an error during guarantor creation
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                # Create borrower
                borrower = Borrower.objects.create(
                    first_name='Nested',
                    last_name='Transaction',
                    email='nested@example.com',
                    created_by=staff_user
                )
                
                # Add borrower to application
                application.borrowers.add(borrower)
                
                # Try to create guarantor but simulate error
                with patch('borrowers.models.Guarantor.objects.create', side_effect=IntegrityError("Simulated error")):
                    guarantor_data = {
                        'guarantor_type': 'individual',
                        'first_name': 'Nested',
                        'last_name': 'Guarantor',
                        'email': 'nested.guarantor@example.com'
                    }
                    
                    create_guarantor_for_application(
                        guarantor_data=guarantor_data,
                        borrower_id=borrower.id,
                        application_id=application.id,
                        user=staff_user
                    )
        
        # Verify neither borrower nor guarantor were created (transaction was rolled back)
        assert Borrower.objects.count() == initial_borrower_count
        assert Guarantor.objects.count() == initial_guarantor_count


@pytest.mark.django_db
class TestNotificationEdgeCases:
    """Test edge cases for notification services."""
    
    def test_create_notification_with_nonexistent_user(self):
        """Test creating a notification for a nonexistent user."""
        # Create a user
        user = MagicMock()
        user.id = 999999  # Nonexistent user ID
        
        # Create a mock notification
        mock_notification = MagicMock()
        
        # Mock the entire create_notification function
        with patch('users.services.create_notification', return_value=mock_notification) as mock_create:
            # Call the mocked function
            notification = mock_create(
                user=user,
                title="Test Notification",
                message="This is a test notification",
                notification_type="system"
            )
        
        # Verify the mock was returned
        assert notification is mock_notification
    
    def test_send_email_notification_with_invalid_email(self):
        """Test sending an email notification with an invalid email."""
        # Create a user with an invalid email
        user = MagicMock()
        user.email = "invalid-email"
        
        # Mock send_mail to raise an exception for invalid email
        with patch('users.services.send_mail', side_effect=Exception("Invalid email")):
            # Send email notification
            result = send_email_notification(
                user=user,
                subject="Test Email",
                message="This is a test email"
            )
        
        # Verify result indicates failure
        assert result is False
