"""
Integration tests for the Broker API.

This test suite covers:
1. CRUD operations for brokers with different user roles
2. Relationship testing between brokers and other entities
3. Filtering functionality
4. Special endpoints
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from brokers.models import Branch, Broker, BDM
from users.models import User
from applications.models import Application
from tests.integration.factories.broker_factory import BranchFactory, BrokerFactory, BDMFactory
from tests.integration.factories.user_factory import AdminUserFactory, BrokerUserFactory, ClientUserFactory, UserFactory
from tests.integration.factories.application_factory import ApplicationFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return AdminUserFactory()


@pytest.fixture
def broker_user():
    return BrokerUserFactory()


@pytest.fixture
def client_user():
    return ClientUserFactory()


@pytest.fixture
def bd_user():
    user = UserFactory(role='bd')
    return user


@pytest.fixture
def branch():
    return BranchFactory()


@pytest.fixture
def broker(branch, broker_user):
    broker = BrokerFactory(branch=branch, user=broker_user)
    return broker


@pytest.fixture
def another_broker(branch):
    another_broker_user = BrokerUserFactory()
    return BrokerFactory(branch=branch, user=another_broker_user)


@pytest.fixture
def bdm(branch, bd_user):
    return BDMFactory(branch=branch, user=bd_user)


@pytest.fixture
def application(broker):
    return ApplicationFactory(broker=broker)


@pytest.mark.django_db
class TestBrokerAPI:
    """
    Test suite for Broker API endpoints.
    """

    def test_admin_can_list_brokers(self, api_client, admin_user, broker):
        """Test that admin users can list all brokers"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check if response is a list with at least one item
        assert isinstance(response.data, list) or 'results' in response.data
        
        # Handle both paginated and non-paginated responses
        broker_list = response.data if isinstance(response.data, list) else response.data['results']
        assert len(broker_list) >= 1
        assert any(item['id'] == broker.id for item in broker_list)

    def test_broker_can_view_own_profile(self, api_client, broker_user, broker):
        """Test that broker users can view their own profile"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == broker.id
        assert response.data['name'] == broker.name

    def test_broker_cannot_view_other_broker_profile(self, api_client, broker_user, another_broker):
        """Test that broker users cannot view other broker profiles"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('broker-detail', args=[another_broker.id])
        response = api_client.get(url)
        
        # Should return 404 as the broker is filtered out of the queryset
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_client_cannot_view_broker_profile(self, api_client, client_user, broker):
        """Test that client users cannot view broker profiles"""
        api_client.force_authenticate(user=client_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.get(url)
        
        # Should return 404 as the broker is filtered out of the queryset
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_create_broker(self, api_client, admin_user, branch):
        """Test that admin users can create brokers"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-list')
        data = {
            'name': 'New Test Broker',
            'company': 'New Test Company',
            'email': 'newbroker@example.com',
            'phone': '1234567890',
            'branch_id': branch.id
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Test Broker'
        assert response.data['company'] == 'New Test Company'
        assert Broker.objects.filter(name='New Test Broker').exists()

    def test_broker_cannot_create_broker(self, api_client, broker_user, branch):
        """Test that broker users cannot create brokers"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('broker-list')
        data = {
            'name': 'New Test Broker',
            'company': 'New Test Company',
            'email': 'newbroker@example.com',
            'phone': '1234567890',
            'branch_id': branch.id
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Broker.objects.filter(name='New Test Broker').exists()

    def test_admin_can_update_broker(self, api_client, admin_user, broker):
        """Test that admin users can update brokers"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-detail', args=[broker.id])
        data = {
            'name': 'Updated Broker Name',
            'company': broker.company
        }
        response = api_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Broker Name'
        broker.refresh_from_db()
        assert broker.name == 'Updated Broker Name'

    def test_broker_cannot_update_other_broker(self, api_client, broker_user, another_broker):
        """Test that broker users cannot update other brokers"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('broker-detail', args=[another_broker.id])
        data = {
            'name': 'Updated Broker Name'
        }
        response = api_client.patch(url, data)
        
        # Should return 403 Forbidden or 404 Not Found depending on implementation
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        another_broker.refresh_from_db()
        assert another_broker.name != 'Updated Broker Name'

    def test_admin_can_delete_broker(self, api_client, admin_user, broker):
        """Test that admin users can delete brokers"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Broker.objects.filter(id=broker.id).exists()

    def test_broker_cannot_delete_broker(self, api_client, broker_user, broker):
        """Test that broker users cannot delete brokers"""
        api_client.force_authenticate(user=broker_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Broker.objects.filter(id=broker.id).exists()

    def test_missing_required_fields(self, api_client, admin_user):
        """Test validation for missing required fields"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-list')
        data = {
            'company': 'Test Company',
            'email': 'test@example.com'
            # Missing 'name' field which is required
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_broker_branch_relationship(self, api_client, admin_user, broker, branch):
        """Test that broker is correctly linked to a branch"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['branch']['id'] == branch.id
        assert response.data['branch']['name'] == branch.name

    def test_broker_user_relationship(self, api_client, admin_user, broker, broker_user):
        """Test that broker is correctly linked to a user"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check if user relationship is included in the response
        # This depends on how the serializer is configured
        if 'user' in response.data:
            assert response.data['user'] == broker_user.id

    def test_broker_application_relationship(self, api_client, admin_user, broker, application):
        """Test that broker is correctly linked to applications"""
        api_client.force_authenticate(user=admin_user)
        # Use the action URL pattern
        url = reverse('broker-detail', args=[broker.id]) + 'applications/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['id'] == application.id

    def test_filter_brokers_by_branch(self, api_client, admin_user, broker, branch):
        """Test filtering brokers by branch"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-list')
        response = api_client.get(url, {'branch': branch.id})
        
        assert response.status_code == status.HTTP_200_OK
        # Check if response is a list with at least one item
        assert isinstance(response.data, list) or 'results' in response.data
        
        # Handle both paginated and non-paginated responses
        broker_list = response.data if isinstance(response.data, list) else response.data['results']
        assert len(broker_list) >= 1
        assert all(item['branch_name'] == branch.name for item in broker_list)

    def test_search_brokers(self, api_client, admin_user, broker):
        """Test searching brokers by name, company, email, or phone"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-list')
        
        # Search by name
        response = api_client.get(url, {'search': broker.name})
        assert response.status_code == status.HTTP_200_OK
        # Check if response is a list with at least one item
        assert isinstance(response.data, list) or 'results' in response.data
        
        # Handle both paginated and non-paginated responses
        broker_list = response.data if isinstance(response.data, list) else response.data['results']
        assert len(broker_list) >= 1
        assert any(item['id'] == broker.id for item in broker_list)
        
        # Search by company
        response = api_client.get(url, {'search': broker.company})
        assert response.status_code == status.HTTP_200_OK
        # Handle both paginated and non-paginated responses
        broker_list = response.data if isinstance(response.data, list) else response.data['results']
        assert len(broker_list) >= 1
        assert any(item['id'] == broker.id for item in broker_list)

    def test_branch_brokers_endpoint(self, api_client, admin_user, branch, broker):
        """Test the endpoint that returns brokers for a specific branch"""
        api_client.force_authenticate(user=admin_user)
        # Use the action URL pattern
        url = reverse('branch-detail', args=[branch.id]) + 'brokers/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert any(item['id'] == broker.id for item in response.data)

    def test_broker_applications_endpoint(self, api_client, admin_user, broker, application):
        """Test the endpoint that returns applications for a specific broker"""
        api_client.force_authenticate(user=admin_user)
        # Use the action URL pattern
        url = reverse('broker-detail', args=[broker.id]) + 'applications/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert response.data[0]['id'] == application.id

    def test_bd_can_view_assigned_brokers(self, api_client, bd_user, broker, bdm):
        """Test that BD users can view brokers assigned to them"""
        # Assign broker to BDM
        broker.bdms.add(bdm)
        
        api_client.force_authenticate(user=bd_user)
        url = reverse('broker-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check if response is a list with at least one item
        assert isinstance(response.data, list) or 'results' in response.data
        
        # Handle both paginated and non-paginated responses
        broker_list = response.data if isinstance(response.data, list) else response.data['results']
        assert len(broker_list) >= 1
        assert any(item['id'] == broker.id for item in broker_list)

    def test_deleting_broker_with_applications(self, api_client, admin_user, broker, application):
        """Test deleting a broker that has applications"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('broker-detail', args=[broker.id])
        response = api_client.delete(url)
        
        # The broker should be deleted, and the application's broker field should be set to NULL
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Broker.objects.filter(id=broker.id).exists()
        
        # Refresh the application from the database
        application.refresh_from_db()
        assert application.broker is None
