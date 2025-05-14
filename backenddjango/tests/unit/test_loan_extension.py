import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from django.contrib.auth import get_user_model
from applications.models import Application
from documents.models import Repayment, Note, Ledger
from datetime import datetime, timedelta

User = get_user_model()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        role='admin'
    )

@pytest.fixture
def application(admin_user):
    return Application.objects.create(
        reference_number='TEST-APP-001',
        loan_amount=Decimal('750000.00'),
        loan_term=360,  # 30 years in months
        interest_rate=Decimal('6.5'),
        repayment_frequency='monthly',
        created_by=admin_user
    )

@pytest.fixture
def repayments(application, admin_user):
    repayments = []
    start_date = datetime.now().date()
    
    # Create 5 repayments for testing
    for i in range(1, 6):
        due_date = start_date.replace(month=((start_date.month + i - 1) % 12) + 1)
        if (start_date.month + i - 1) // 12 > 0:
            due_date = due_date.replace(year=due_date.year + (start_date.month + i - 1) // 12)
        
        repayment = Repayment.objects.create(
            application=application,
            amount=Decimal('4500.00'),
            due_date=due_date,
            created_by=admin_user
        )
        repayments.append(repayment)
    
    return repayments

@pytest.fixture
def api_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client

@pytest.mark.django_db
def test_extend_loan_success(api_client, application, repayments):
    """Test successful loan extension"""
    url = reverse('application-extend-loan', kwargs={'pk': application.id})
    
    # Initial values
    initial_loan_amount = application.loan_amount
    initial_interest_rate = application.interest_rate
    initial_repayment_amount = repayments[0].amount
    initial_repayment_count = Repayment.objects.filter(application=application).count()
    
    # New values for loan extension
    data = {
        'new_rate': '7.25',
        'new_loan_amount': '850000.00',
        'new_repayment': '15000.00'
    }
    
    response = api_client.post(url, data, format='json')
    
    # Check response status
    assert response.status_code == status.HTTP_200_OK
    
    # Check that application was updated
    application.refresh_from_db()
    assert application.loan_amount == Decimal('850000.00')
    assert application.interest_rate == Decimal('7.25')
    
    # Check that old repayments were deleted and new ones created
    new_repayments = Repayment.objects.filter(application=application)
    assert new_repayments.count() > 0
    assert new_repayments.count() != initial_repayment_count
    
    # Check that the first repayment has the new amount
    first_repayment = new_repayments.order_by('due_date').first()
    assert first_repayment.amount == Decimal('15000.00')
    
    # Check that a note was created
    notes = Note.objects.filter(application=application, title="Loan Extension")
    assert notes.count() == 1
    
    # Check that a ledger entry was created
    ledger_entries = Ledger.objects.filter(
        application=application,
        transaction_type='adjustment'
    )
    assert ledger_entries.count() == 1

@pytest.mark.django_db
def test_extend_loan_invalid_data(api_client, application):
    """Test loan extension with invalid data"""
    url = reverse('application-extend-loan', kwargs={'pk': application.id})
    
    # Test with negative interest rate
    data = {
        'new_rate': '-1.0',
        'new_loan_amount': '850000.00',
        'new_repayment': '15000.00'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'new_rate' in response.data
    
    # Test with negative loan amount
    data = {
        'new_rate': '7.25',
        'new_loan_amount': '-100.00',
        'new_repayment': '15000.00'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'new_loan_amount' in response.data
    
    # Test with repayment greater than loan amount
    data = {
        'new_rate': '7.25',
        'new_loan_amount': '10000.00',
        'new_repayment': '15000.00'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'new_repayment' in response.data

@pytest.mark.django_db
def test_extend_loan_nonexistent_application(api_client):
    """Test loan extension with non-existent application"""
    url = reverse('application-extend-loan', kwargs={'pk': 99999})
    
    data = {
        'new_rate': '7.25',
        'new_loan_amount': '850000.00',
        'new_repayment': '15000.00'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_extend_loan_unauthorized(application, repayments):
    """Test loan extension with unauthorized user"""
    # Create a non-admin user
    user = User.objects.create_user(
        username='regularuser',
        email='user@example.com',
        password='userpass123',
        first_name='Regular',
        last_name='User',
        role='client'
    )
    
    # Create client and authenticate with non-admin user
    client = APIClient()
    client.force_authenticate(user=user)
    
    url = reverse('application-extend-loan', kwargs={'pk': application.id})
    
    data = {
        'new_rate': '7.25',
        'new_loan_amount': '850000.00',
        'new_repayment': '15000.00'
    }
    
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN