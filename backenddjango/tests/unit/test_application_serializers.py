"""
Unit tests for application serializers.
"""

import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from applications.serializers import (
    ApplicationDetailSerializer,
    ApplicationCreateSerializer,
    ApplicationStageUpdateSerializer,
    ApplicationBorrowerSerializer,
    BorrowerSerializer,
    AddressSerializer,
    EmploymentInfoSerializer
)
from applications.models import Application
from borrowers.models import Borrower


@pytest.mark.django_db
class TestAddressSerializer:
    """Test the AddressSerializer."""
    
    def test_address_serializer_fields(self):
        """Test that the serializer includes the expected fields."""
        data = {
            'street': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postal_code': '12345',
            'country': 'Test Country'
        }
        
        serializer = AddressSerializer(data=data)
        assert serializer.is_valid()
        
        # Check that all fields are included
        assert set(serializer.validated_data.keys()) == {
            'street', 'city', 'state', 'postal_code', 'country'
        }


@pytest.mark.django_db
class TestEmploymentInfoSerializer:
    """Test the EmploymentInfoSerializer."""
    
    def test_employment_info_serializer_fields(self):
        """Test that the serializer includes the expected fields."""
        data = {
            'employer': 'Test Employer',
            'position': 'Test Position',
            'income': '75000.00',
            'years_employed': '5.5'
        }
        
        serializer = EmploymentInfoSerializer(data=data)
        assert serializer.is_valid()
        
        # Check that all fields are included
        assert set(serializer.validated_data.keys()) == {
            'employer', 'position', 'income', 'years_employed'
        }


@pytest.mark.django_db
class TestBorrowerSerializer:
    """Test the BorrowerSerializer."""
    
    def test_borrower_serializer_fields(self, individual_borrower):
        """Test that the serializer includes the expected fields."""
        serializer = BorrowerSerializer(individual_borrower)
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'employment_info',
            'tax_id', 'marital_status', 'residency_status',
            'referral_source', 'tags'
        }
        
        assert data['first_name'] == individual_borrower.first_name
        assert data['last_name'] == individual_borrower.last_name
        assert data['email'] == individual_borrower.email
    
    def test_get_address_method(self, individual_borrower):
        """Test the get_address method."""
        # Set a residential address
        individual_borrower.residential_address = '123 Test St'
        individual_borrower.save()
        
        serializer = BorrowerSerializer(individual_borrower)
        address = serializer.get_address(individual_borrower)
        
        assert address['street'] == '123 Test St'
        assert address['city'] == ''
        assert address['state'] == ''
        assert address['postal_code'] == ''
        assert address['country'] == ''
    
    def test_get_employment_info_method(self, individual_borrower):
        """Test the get_employment_info method."""
        # Set employment info
        individual_borrower.employer_name = 'Test Employer'
        individual_borrower.job_title = 'Test Position'
        individual_borrower.annual_income = 75000
        individual_borrower.employment_duration = 5.5
        individual_borrower.save()
        
        serializer = BorrowerSerializer(individual_borrower)
        employment_info = serializer.get_employment_info(individual_borrower)
        
        assert employment_info['employer'] == 'Test Employer'
        assert employment_info['position'] == 'Test Position'
        assert employment_info['income'] == 75000
        assert employment_info['years_employed'] == 5.5


@pytest.mark.django_db
class TestApplicationCreateSerializer:
    """Test the ApplicationCreateSerializer."""
    
    def test_application_create_serializer_fields(self):
        """Test that the serializer includes the expected fields."""
        data = {
            'reference_number': 'APP-TEST-001',
            'stage': 'inquiry',
            'loan_amount': '500000.00',
            'loan_term': 360,
            'interest_rate': '4.5',
            'purpose': 'Home purchase',
            'application_type': 'residential'
        }
        
        serializer = ApplicationCreateSerializer(data=data)
        assert serializer.is_valid()
        
        # Check that all fields are included
        assert set(serializer.validated_data.keys()) >= {
            'reference_number', 'stage', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'application_type'
        }
    
    def test_create_application(self, broker_user):
        """Test creating an application with the serializer."""
        factory = APIRequestFactory()
        request = factory.post('/api/applications/')
        request.user = broker_user
        
        data = {
            'reference_number': 'APP-TEST-001',
            'stage': 'inquiry',
            'loan_amount': '500000.00',
            'loan_term': 360,
            'interest_rate': '4.5',
            'purpose': 'Home purchase',
            'application_type': 'residential'
        }
        
        serializer = ApplicationCreateSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        
        application = serializer.save(created_by=broker_user)
        assert application.reference_number == 'APP-TEST-001'
        assert application.stage == 'inquiry'
        assert application.loan_amount == 500000.00
        assert application.loan_term == 360
        assert application.interest_rate == 4.5
        assert application.purpose == 'Home purchase'
        assert application.application_type == 'residential'
        assert application.created_by == broker_user


@pytest.mark.django_db
class TestApplicationDetailSerializer:
    """Test the ApplicationDetailSerializer."""
    
    def test_application_detail_serializer_fields(self, application, broker, bdm):
        """Test that the serializer includes the expected fields."""
        # Set broker and BD for the application
        application.broker = broker
        application.bd = bdm
        application.save()
        
        # Create a request context
        request = RequestFactory().get('/')
        
        serializer = ApplicationDetailSerializer(application, context={'request': request})
        data = serializer.data
        
        assert set(data.keys()) >= {
            'id', 'reference_number', 'stage', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'application_type', 'broker',
            'bd', 'created_by', 'created_at', 'updated_at'
        }
        
        assert data['reference_number'] == application.reference_number
        assert data['stage'] == application.stage
        assert data['loan_amount'] == str(application.loan_amount)
        assert data['loan_term'] == application.loan_term
        assert data['interest_rate'] == str(application.interest_rate)
        assert data['purpose'] == application.purpose
        assert data['application_type'] == application.application_type
    
    def test_nested_serializers(self, application, broker, bdm):
        """Test that nested serializers are included."""
        # Set broker and BD for the application
        application.broker = broker
        application.bd = bdm
        application.save()
        
        # Create a request context
        request = RequestFactory().get('/')
        
        serializer = ApplicationDetailSerializer(application, context={'request': request})
        data = serializer.data
        
        # Check that broker and bd are serialized
        assert 'broker' in data
        assert 'bd' in data
        assert data['broker']['id'] == broker.id
        assert data['bd']['id'] == bdm.id


@pytest.mark.django_db
class TestApplicationStageUpdateSerializer:
    """Test the ApplicationStageUpdateSerializer."""
    
    def test_application_stage_update_serializer_fields(self):
        """Test that the serializer includes the expected fields."""
        data = {
            'stage': 'assessment',
            'notes': 'Moving to assessment stage'
        }
        
        serializer = ApplicationStageUpdateSerializer(data=data)
        assert serializer.is_valid()
        
        # Check that all fields are included
        assert set(serializer.validated_data.keys()) == {'stage', 'notes'}
    
    def test_validate_stage(self):
        """Test stage validation."""
        # Valid stage
        data = {
            'stage': 'assessment',
            'notes': 'Moving to assessment stage'
        }
        
        serializer = ApplicationStageUpdateSerializer(data=data)
        assert serializer.is_valid()
        
        # Invalid stage
        data = {
            'stage': 'invalid_stage',
            'notes': 'Moving to invalid stage'
        }
        
        serializer = ApplicationStageUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'stage' in serializer.errors


@pytest.mark.django_db
class TestApplicationBorrowerSerializer:
    """Test the ApplicationBorrowerSerializer."""
    
    def test_application_borrower_serializer_fields(self):
        """Test that the serializer includes the expected fields."""
        data = {
            'borrowers': [1, 2, 3]
        }
        
        serializer = ApplicationBorrowerSerializer(data=data)
        assert serializer.is_valid()
        
        # Check that all fields are included
        assert set(serializer.validated_data.keys()) == {'borrowers'}
    
    def test_update_application_borrowers(self, application, individual_borrower, company_borrower):
        """Test updating application borrowers."""
        # Create a request context
        request = RequestFactory().put('/')
        
        data = {
            'borrowers': [individual_borrower.id, company_borrower.id]
        }
        
        serializer = ApplicationBorrowerSerializer(
            application,
            data=data,
            context={'request': request}
        )
        assert serializer.is_valid()
        
        updated_application = serializer.save()
        
        # Check that borrowers were updated
        borrower_ids = list(updated_application.borrowers.values_list('id', flat=True))
        assert individual_borrower.id in borrower_ids
        assert company_borrower.id in borrower_ids
