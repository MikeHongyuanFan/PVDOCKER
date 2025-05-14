"""
Unit tests for application services.
"""

import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
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
from users.models import Notification


@pytest.mark.django_db
class TestApplicationValidationService:
    """Test the application validation service."""
    
    def test_validate_valid_application(self):
        """Test validation with valid application data."""
        valid_data = {
            "loan_amount": 500000,
            "loan_term": 360,
            "interest_rate": 4.5,
            "purpose": "Home purchase",
            "application_type": "residential",
            "repayment_frequency": "monthly",
            "estimated_settlement_date": "2025-06-01"
        }
        
        is_valid, errors = validate_application_schema(valid_data)
        assert is_valid is True
        assert errors is None
    
    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        invalid_data = {
            "loan_amount": 500000,
            # Missing loan_term
            "interest_rate": 4.5,
            # Missing purpose
            "application_type": "residential"
        }
        
        is_valid, errors = validate_application_schema(invalid_data)
        assert is_valid is False
        assert "loan_term" in errors.lower() or "purpose" in errors.lower()
    
    def test_validate_invalid_field_values(self):
        """Test validation with invalid field values."""
        invalid_data = {
            "loan_amount": -5000,  # Negative amount
            "loan_term": 0,  # Zero term
            "interest_rate": -1,  # Negative rate
            "purpose": "Buy",
            "application_type": "residential",
            "repayment_frequency": "invalid_frequency"  # Invalid enum value
        }
        
        is_valid, errors = validate_application_schema(invalid_data)
        assert is_valid is False


@pytest.mark.django_db
class TestApplicationStageService:
    """Test the application stage update service."""
    
    def test_update_application_stage(self, staff_user):
        """Test updating an application's stage."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-001",
            stage="inquiry",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Update the stage
        with patch('applications.services.create_application_notification') as mock_notify:
            updated_app = update_application_stage(application.id, "assessment", staff_user)
        
        # Verify the stage was updated
        assert updated_app.stage == "assessment"
        
        # Verify a note was created
        note = Note.objects.filter(application=application).first()
        assert note is not None
        assert "inquiry" in note.content
        assert "assessment" in note.content
        
        # Verify notification function was called
        mock_notify.assert_called_once()
    
    def test_update_application_stage_invalid_id(self, staff_user):
        """Test updating a non-existent application's stage."""
        with pytest.raises(ValueError):
            update_application_stage(999999, "assessment", staff_user)


@pytest.mark.django_db
class TestSignatureProcessingService:
    """Test the signature processing service."""
    
    def test_process_signature_data(self, staff_user):
        """Test processing signature data for an application."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-002",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Mock signature data (base64 encoded)
        signature_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        signed_by = "John Doe"
        
        # Process signature
        updated_app = process_signature_data(application.id, signature_data, signed_by, staff_user)
        
        # Verify the signature was processed
        assert updated_app.signed_by == "John Doe"
        assert updated_app.signature_date is not None
        
        # Verify a note was created
        note = Note.objects.filter(application=application).first()
        assert note is not None
        assert "signed by John Doe" in note.content
    
    def test_process_signature_invalid_id(self, staff_user):
        """Test processing signature for a non-existent application."""
        signature_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        with pytest.raises(ValueError):
            process_signature_data(999999, signature_data, "John Doe", staff_user)


@pytest.mark.django_db
class TestDocumentGenerationService:
    """Test the document generation service."""
    
    def test_generate_document(self, staff_user, individual_borrower):
        """Test generating a document for an application."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-003",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(individual_borrower)
        
        # Mock file operations
        with patch('os.makedirs') as mock_makedirs, \
             patch('os.path.getsize') as mock_getsize, \
             patch('builtins.open') as mock_open:
            
            mock_makedirs.return_value = None
            mock_getsize.return_value = 1024  # 1KB file size
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            
            # Generate document
            document = generate_document(application.id, "application_form", staff_user)
        
        # Verify document was created
        assert document is not None
        assert document.title == f"Application Form - {application.reference_number}"
        assert document.document_type == "application_form"
        assert document.application == application
        assert document.created_by == staff_user
        assert document.file_size == 1024
        assert document.file_type == "application/pdf"
    
    def test_generate_document_invalid_id(self, staff_user):
        """Test generating a document for a non-existent application."""
        document = generate_document(999999, "application_form", staff_user)
        assert document is None
    
    def test_generate_document_invalid_type(self, staff_user, individual_borrower):
        """Test generating a document with an invalid type."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-004",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Add borrower to application
        application.borrowers.add(individual_borrower)
        
        # Generate document with invalid type
        document = generate_document(application.id, "invalid_type", staff_user)
        assert document is None


@pytest.mark.django_db
class TestRepaymentScheduleService:
    """Test the repayment schedule generation service."""
    
    def test_generate_repayment_schedule(self, staff_user):
        """Test generating a repayment schedule for an application."""
        # Create an application with settlement date
        settlement_date = timezone.now().date()
        application = Application.objects.create(
            reference_number="APP-TEST-005",
            stage="approved",
            loan_amount=500000,
            loan_term=12,  # 12 months for easier testing
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            repayment_frequency="monthly",
            estimated_settlement_date=settlement_date,
            created_by=staff_user
        )
        
        # Generate repayment schedule
        repayments = generate_repayment_schedule(application.id, staff_user)
        
        # Verify repayments were created
        assert len(repayments) == 12  # One for each month
        
        # Verify first repayment
        first_repayment = repayments[0]
        assert first_repayment.application == application
        assert first_repayment.created_by == staff_user
        assert first_repayment.amount > 0
        
        # Verify all repayments have due dates
        for repayment in repayments:
            assert repayment.due_date is not None
    
    def test_generate_repayment_schedule_no_interest(self, staff_user):
        """Test generating a repayment schedule with no interest."""
        # Create an application with settlement date
        settlement_date = timezone.now().date()
        application = Application.objects.create(
            reference_number="APP-TEST-006",
            stage="approved",
            loan_amount=12000,  # $12,000 for easy division
            loan_term=12,  # 12 months for easier testing
            interest_rate=0,  # No interest
            purpose="Home purchase",
            application_type="residential",
            repayment_frequency="monthly",
            estimated_settlement_date=settlement_date,
            created_by=staff_user
        )
        
        # Generate repayment schedule
        repayments = generate_repayment_schedule(application.id, staff_user)
        
        # Verify repayments were created
        assert len(repayments) == 12  # One for each month
        
        # Verify equal payments of $1,000 each
        for repayment in repayments:
            assert repayment.amount == 1000.0
    
    def test_generate_repayment_schedule_invalid_id(self, staff_user):
        """Test generating a repayment schedule for a non-existent application."""
        repayments = generate_repayment_schedule(999999, staff_user)
        assert len(repayments) == 0


@pytest.mark.django_db
class TestFeeCreationService:
    """Test the fee creation service."""
    
    def test_create_standard_fees(self, staff_user):
        """Test creating standard fees for an application."""
        # Create an application
        application = Application.objects.create(
            reference_number="APP-TEST-007",
            stage="approved",
            loan_amount=500000,
            loan_term=360,
            interest_rate=4.5,
            purpose="Home purchase",
            application_type="residential",
            created_by=staff_user
        )
        
        # Create standard fees
        fees = create_standard_fees(application.id, staff_user)
        
        # Verify fees were created
        assert len(fees) == 4  # Four standard fees
        
        # Verify fee types
        fee_types = [fee.fee_type for fee in fees]
        assert "application" in fee_types
        assert "valuation" in fee_types
        assert "legal" in fee_types
        assert "settlement" in fee_types
        
        # Verify fee amounts
        for fee in fees:
            assert fee.amount > 0
            assert fee.application == application
            assert fee.created_by == staff_user
            assert fee.due_date is not None
    
    def test_create_standard_fees_invalid_id(self, staff_user):
        """Test creating standard fees for a non-existent application."""
        fees = create_standard_fees(999999, staff_user)
        assert len(fees) == 0
