import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from brokers.models import Branch, Broker, BDM
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email='admin@example.com',
        password='password123',
        role='admin'
    )


@pytest.fixture
def branch():
    return Branch.objects.create(
        name='Test Branch',
        address='123 Test St',
        phone='1234567890',
        email='branch@example.com'
    )


@pytest.fixture
def broker(branch):
    return Broker.objects.create(
        name='Test Broker',
        company='Test Company',
        email='broker@example.com',
        phone='0987654321',
        branch=branch
    )


@pytest.fixture
def bdm(branch):
    return BDM.objects.create(
        name='Test BDM',
        email='bdm@example.com',
        phone='1122334455',
        branch=branch
    )


@pytest.mark.django_db
class TestBranchAPI:
    def test_get_branch_brokers(self, api_client, admin_user, branch, broker):
        """Test getting brokers for a branch"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('branch-brokers', args=[branch.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == broker.id
        assert response.data[0]['name'] == broker.name

    def test_get_branch_bdms(self, api_client, admin_user, branch, bdm):
        """Test getting BDMs for a branch"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('branch-bdms', args=[branch.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == bdm.id
        assert response.data[0]['name'] == bdm.name