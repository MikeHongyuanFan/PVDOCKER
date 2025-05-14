"""
Unit tests for document serializers.
"""

import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from documents.serializers import (
    DocumentSerializer,
    NoteSerializer,
    FeeSerializer,
    RepaymentSerializer,
    LedgerSerializer
)
from documents.models import Document, Note, Fee, Repayment, Ledger
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestDocumentSerializer:
    """Test the DocumentSerializer."""
    
    def test_document_serializer_fields(self, staff_user, application):
        """Test that the serializer includes the expected fields."""
        # Create a test document
        document = Document.objects.create(
            title="Test Document",
            document_type="contract",
            application=application,
            created_by=staff_user
        )
        
        # Create a request context
        request = RequestFactory().get('/')
        
        serializer = DocumentSerializer(document, context={'request': request})
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'title', 'document_type', 'document_type_display',
            'application', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'file_url'
        }
        
        assert data['title'] == document.title
        assert data['document_type'] == document.document_type
        assert data['document_type_display'] == document.get_document_type_display()
        assert data['created_by_name'] == str(staff_user)
    
    def test_file_url_method(self, staff_user, application):
        """Test the file_url method."""
        # Create a test document with a file
        test_file = SimpleUploadedFile(
            "test_file.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        document = Document.objects.create(
            title="Test Document",
            document_type="contract",
            application=application,
            file=test_file,
            created_by=staff_user
        )
        
        # Create a request context
        request = RequestFactory().get('/')
        
        serializer = DocumentSerializer(document, context={'request': request})
        
        # The file_url should not be None
        assert serializer.data['file_url'] is not None
        
        # Test with no file
        document.file = None
        document.save()
        
        serializer = DocumentSerializer(document, context={'request': request})
        assert serializer.data['file_url'] is None
        
        # Test with no request in context
        serializer = DocumentSerializer(document)
        assert serializer.data['file_url'] is None


@pytest.mark.django_db
class TestNoteSerializer:
    """Test the NoteSerializer."""
    
    def test_note_serializer_fields(self, staff_user, application):
        """Test that the serializer includes the expected fields."""
        # Create a test note
        note = Note.objects.create(
            title="Test Note",
            content="This is a test note",
            application=application,
            created_by=staff_user
        )
        
        serializer = NoteSerializer(note)
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'title', 'content', 'application',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        }
        
        assert data['title'] == note.title
        assert data['content'] == note.content
        assert data['created_by_name'] == str(staff_user)
    
    def test_create_note(self, staff_user, application):
        """Test creating a note with the serializer."""
        factory = APIRequestFactory()
        request = factory.post('/api/notes/')
        request.user = staff_user
        
        data = {
            'title': 'New Note',
            'content': 'This is a new note',
            'application': application.id
        }
        
        serializer = NoteSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        
        note = serializer.save(created_by=staff_user)
        assert note.title == 'New Note'
        assert note.content == 'This is a new note'
        assert note.application == application
        assert note.created_by == staff_user


@pytest.mark.django_db
class TestFeeSerializer:
    """Test the FeeSerializer."""
    
    def test_fee_serializer_fields(self, staff_user, application):
        """Test that the serializer includes the expected fields."""
        # Create a test fee
        fee = Fee.objects.create(
            fee_type="application",
            amount=1000.00,
            application=application,
            created_by=staff_user
        )
        
        serializer = FeeSerializer(fee)
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'fee_type', 'fee_type_display', 'amount',
            'application', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'status', 'invoice_url'
        }
        
        assert data['fee_type'] == fee.fee_type
        assert data['fee_type_display'] == fee.get_fee_type_display()
        assert data['amount'] == '1000.00'
        assert data['created_by_name'] == str(staff_user)
    
    def test_status_method(self, staff_user, application):
        """Test the status method."""
        # Create a test fee
        fee = Fee.objects.create(
            fee_type="application",
            amount=1000.00,
            application=application,
            created_by=staff_user
        )
        
        serializer = FeeSerializer(fee)
        
        # The status should be 'unpaid' by default
        assert serializer.get_status(fee) == 'unpaid'
        
        # Set paid_date and test again
        from django.utils import timezone
        fee.paid_date = timezone.now()
        fee.save()
        
        serializer = FeeSerializer(fee)
        assert serializer.get_status(fee) == 'paid'


@pytest.mark.django_db
class TestRepaymentSerializer:
    """Test the RepaymentSerializer."""
    
    def test_repayment_serializer_fields(self, staff_user, application):
        """Test that the serializer includes the expected fields."""
        # Create a test repayment
        from django.utils import timezone
        from datetime import timedelta
        
        due_date = timezone.now().date() + timedelta(days=30)
        repayment = Repayment.objects.create(
            amount=500.00,
            due_date=due_date,
            application=application,
            created_by=staff_user
        )
        
        serializer = RepaymentSerializer(repayment)
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'amount', 'due_date', 'application',
            'created_by', 'created_at', 'updated_at'
        }
        
        assert data['amount'] == '500.00'
        assert data['due_date'] == due_date.isoformat()
    
    def test_create_repayment(self, staff_user, application):
        """Test creating a repayment with the serializer."""
        factory = APIRequestFactory()
        request = factory.post('/api/repayments/')
        request.user = staff_user
        
        from django.utils import timezone
        from datetime import timedelta
        
        due_date = timezone.now().date() + timedelta(days=30)
        data = {
            'amount': 500.00,
            'due_date': due_date.isoformat(),
            'application': application.id
        }
        
        serializer = RepaymentSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        
        repayment = serializer.save(created_by=staff_user)
        assert repayment.amount == 500.00
        assert repayment.due_date == due_date
        assert repayment.application == application
        assert repayment.created_by == staff_user


@pytest.mark.django_db
class TestLedgerSerializer:
    """Test the LedgerSerializer."""
    
    def test_ledger_serializer_fields(self, staff_user, application):
        """Test that the serializer includes the expected fields."""
        # Create a test ledger entry
        ledger = Ledger.objects.create(
            entry_type="debit",
            amount=1000.00,
            description="Test ledger entry",
            application=application,
            created_by=staff_user
        )
        
        serializer = LedgerSerializer(ledger)
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'entry_type', 'amount', 'description',
            'application', 'created_by', 'created_at'
        }
        
        assert data['entry_type'] == ledger.entry_type
        assert data['amount'] == '1000.00'
        assert data['description'] == ledger.description
