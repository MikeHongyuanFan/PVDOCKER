from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from brokers.models import BDM, Branch
from users.serializers import UserCreateSerializer


class BDUserCreationTests(APITestCase):
    def setUp(self):
        # Create an admin user for testing
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # Create a test branch
        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Test St',
            phone='1234567890',
            email='branch@test.com'
        )

    def test_create_bd_user_with_branch(self):
        """
        Test creating a BD user with branch assignment creates both User and BDM records
        """
        url = reverse('user-list')  # Assuming you're using ViewSet URLs
        data = {
            'email': 'bd@test.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'BD',
            'role': 'bd',
            'phone': '9876543210',
            'branch_id': self.branch.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify User was created
        user = User.objects.get(email='bd@test.com')
        self.assertEqual(user.role, 'bd')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'BD')

        # Verify BDM was created
        bdm = BDM.objects.get(user=user)
        self.assertEqual(bdm.name, 'Test BD')
        self.assertEqual(bdm.email, 'bd@test.com')
        self.assertEqual(bdm.phone, '9876543210')
        self.assertEqual(bdm.branch, self.branch)

    def test_create_bd_user_without_branch(self):
        """
        Test creating a BD user without branch assignment
        """
        url = reverse('user-list')
        data = {
            'email': 'bd2@test.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'BD2',
            'role': 'bd',
            'phone': '9876543210'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify User was created
        user = User.objects.get(email='bd2@test.com')
        self.assertEqual(user.role, 'bd')

        # Verify BDM was created without branch
        bdm = BDM.objects.get(user=user)
        self.assertEqual(bdm.name, 'Test BD2')
        self.assertIsNone(bdm.branch)

    def test_create_bd_user_with_invalid_branch(self):
        """
        Test creating a BD user with invalid branch ID
        """
        url = reverse('user-list')
        data = {
            'email': 'bd3@test.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'BD3',
            'role': 'bd',
            'phone': '9876543210',
            'branch_id': 99999  # Non-existent branch ID
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify User was created
        user = User.objects.get(email='bd3@test.com')
        self.assertEqual(user.role, 'bd')

        # Verify BDM was created without branch
        bdm = BDM.objects.get(user=user)
        self.assertEqual(bdm.name, 'Test BD3')
        self.assertIsNone(bdm.branch)

    def test_create_non_bd_user(self):
        """
        Test creating a non-BD user doesn't create BDM record
        """
        url = reverse('user-list')
        data = {
            'email': 'broker@test.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'Broker',
            'role': 'broker',
            'phone': '9876543210',
            'branch_id': self.branch.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify User was created
        user = User.objects.get(email='broker@test.com')
        self.assertEqual(user.role, 'broker')

        # Verify no BDM was created
        self.assertEqual(BDM.objects.filter(user=user).count(), 0)

    def test_create_bd_user_minimal_data(self):
        """
        Test creating a BD user with minimal data
        """
        url = reverse('user-list')
        data = {
            'email': 'bd4@test.com',
            'password': 'testpass123',
            'role': 'bd'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify User was created
        user = User.objects.get(email='bd4@test.com')
        self.assertEqual(user.role, 'bd')

        # Verify BDM was created with email as name
        bdm = BDM.objects.get(user=user)
        self.assertEqual(bdm.name, 'bd4@test.com')
        self.assertEqual(bdm.email, 'bd4@test.com')
