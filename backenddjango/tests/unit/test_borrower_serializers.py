"""
Unit tests for borrower serializers.
"""

import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from borrowers.serializers import (
    BorrowerListSerializer,
    BorrowerDetailSerializer,
    GuarantorSerializer
)
from borrowers.models import Borrower, Guarantor


@pytest.mark.django_db
class TestBorrowerListSerializer:
    """Test the BorrowerListSerializer."""
    
    def test_borrower_list_serializer_fields(self, individual_borrower):
        """Test that the serializer includes the expected fields."""
        serializer = BorrowerListSerializer(individual_borrower)
        data = serializer.data
        
        assert set(data.keys()) == {
            'id', 'first_name', 'last_name', 'email', 
            'phone', 'created_at', 'application_count'
        }
        
        assert data['first_name'] == individual_borrower.first_name
        assert data['last_name'] == individual_borrower.last_name
        assert data['email'] == individual_borrower.email
        assert data['phone'] == individual_borrower.phone
    
    def test_application_count_method(self, individual_borrower, application):
        """Test the application_count method."""
        # Add borrower to application
        application.borrowers.add(individual_borrower)
        
        serializer = BorrowerListSerializer(individual_borrower)
        assert serializer.data['application_count'] == 1


@pytest.mark.django_db
class TestBorrowerDetailSerializer:
    """Test the BorrowerDetailSerializer."""
    
    def test_borrower_detail_serializer_fields(self, individual_borrower):
        """Test that the serializer includes all fields."""
        serializer = BorrowerDetailSerializer(individual_borrower)
        data = serializer.data
        
        # Check that all model fields are included
        assert 'id' in data
        assert 'first_name' in data
        assert 'last_name' in data
        assert 'email' in data
        assert 'phone' in data
        assert 'residential_address' in data
        assert 'date_of_birth' in data
        assert 'created_by' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_borrower(self, staff_user):
        """Test creating a borrower with the serializer."""
        factory = APIRequestFactory()
        request = factory.post('/api/borrowers/')
        request.user = staff_user
        
        data = {
            'first_name': 'Test',
            'last_name': 'Borrower',
            'email': 'test.borrower@example.com',
            'phone': '1234567890',
            'residential_address': '123 Test St',
            'date_of_birth': '1980-01-01',
            'employment_type': 'full_time',
            'annual_income': 75000
        }
        
        serializer = BorrowerDetailSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        
        borrower = serializer.save()
        assert borrower.first_name == 'Test'
        assert borrower.last_name == 'Borrower'
        assert borrower.email == 'test.borrower@example.com'
        assert borrower.created_by == staff_user
    
    def test_update_borrower(self, individual_borrower, staff_user):
        """Test updating a borrower with the serializer."""
        factory = APIRequestFactory()
        request = factory.put('/api/borrowers/1/')
        request.user = staff_user
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Borrower',
            'email': individual_borrower.email,
            'phone': individual_borrower.phone,
            'residential_address': individual_borrower.residential_address,
            'date_of_birth': individual_borrower.date_of_birth,
            'employment_type': individual_borrower.employment_type,
            'annual_income': individual_borrower.annual_income
        }
        
        serializer = BorrowerDetailSerializer(
            individual_borrower, 
            data=data, 
            context={'request': request},
            partial=True
        )
        assert serializer.is_valid()
        
        updated_borrower = serializer.save()
        assert updated_borrower.first_name == 'Updated'
        assert updated_borrower.last_name == 'Borrower'


@pytest.mark.django_db
class TestGuarantorSerializer:
    """Test the GuarantorSerializer."""
    
    def test_guarantor_serializer_fields(self, staff_user, individual_borrower, application):
        """Test that the serializer includes all fields."""
        guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Test',
            last_name='Guarantor',
            email='test.guarantor@example.com',
            phone='1234567890',
            borrower=individual_borrower,
            application=application,
            created_by=staff_user
        )
        
        serializer = GuarantorSerializer(guarantor)
        data = serializer.data
        
        # Check that all model fields are included
        assert 'id' in data
        assert 'guarantor_type' in data
        assert 'first_name' in data
        assert 'last_name' in data
        assert 'email' in data
        assert 'phone' in data
        assert 'borrower' in data
        assert 'application' in data
        assert 'created_by' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_guarantor(self, staff_user, individual_borrower, application):
        """Test creating a guarantor with the serializer."""
        factory = APIRequestFactory()
        request = factory.post('/api/guarantors/')
        request.user = staff_user
        
        data = {
            'guarantor_type': 'individual',
            'first_name': 'Test',
            'last_name': 'Guarantor',
            'email': 'test.guarantor@example.com',
            'phone': '1234567890',
            'borrower': individual_borrower.id,
            'application': application.id
        }
        
        serializer = GuarantorSerializer(data=data, context={'request': request})
        assert serializer.is_valid()
        
        guarantor = serializer.save()
        assert guarantor.first_name == 'Test'
        assert guarantor.last_name == 'Guarantor'
        assert guarantor.email == 'test.guarantor@example.com'
        assert guarantor.created_by == staff_user
        assert guarantor.borrower == individual_borrower
        assert guarantor.application == application
    
    def test_update_guarantor(self, staff_user, individual_borrower, application):
        """Test updating a guarantor with the serializer."""
        guarantor = Guarantor.objects.create(
            guarantor_type='individual',
            first_name='Test',
            last_name='Guarantor',
            email='test.guarantor@example.com',
            phone='1234567890',
            borrower=individual_borrower,
            application=application,
            created_by=staff_user
        )
        
        factory = APIRequestFactory()
        request = factory.put('/api/guarantors/1/')
        request.user = staff_user
        
        data = {
            'guarantor_type': 'individual',
            'first_name': 'Updated',
            'last_name': 'Guarantor',
            'email': guarantor.email,
            'phone': guarantor.phone,
            'borrower': guarantor.borrower.id,
            'application': guarantor.application.id
        }
        
        serializer = GuarantorSerializer(
            guarantor, 
            data=data, 
            context={'request': request},
            partial=True
        )
        assert serializer.is_valid()
        
        updated_guarantor = serializer.save()
        assert updated_guarantor.first_name == 'Updated'
        assert updated_guarantor.last_name == 'Guarantor'
