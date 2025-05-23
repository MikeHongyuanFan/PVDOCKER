from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from applications.models import Application
from brokers.models import BDM
from users.models import Notification
from documents.models import Note

User = get_user_model()

class BDAssignmentTests(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        self.bd_user = User.objects.create_user(
            email='bd@test.com',
            password='testpass123',
            role='bd'
        )
        self.other_bd_user = User.objects.create_user(
            email='otherbd@test.com',
            password='testpass123',
            role='bd'
        )
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            role='client'
        )

        # Create a test application
        self.application = Application.objects.create(
            loan_amount=100000,
            loan_term=12,
            created_by=self.admin_user
        )

        # Set up API client
        self.client = APIClient()

    def test_assign_bd_to_application(self):
        """Test assigning a BD to an application"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        response = self.client.post(url, {'bd_id': self.bd_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify application was updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)
        
        # Verify notification was created
        self.assertTrue(Notification.objects.filter(
            user=self.bd_user,
            notification_type='application_status'
        ).exists())
        
        # Verify note was created
        self.assertTrue(Note.objects.filter(
            application=self.application,
            created_by=self.admin_user
        ).exists())

    def test_assign_bd_to_already_assigned_application(self):
        """Test assigning a BD to an application that already has one"""
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        response = self.client.post(url, {'bd_id': self.other_bd_user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify assignment didn't change
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)

    def test_update_bd_assignment(self):
        """Test updating a BD assignment with PUT method"""
        # First assign a BD
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        # Now update the assignment to a different BD
        response = self.client.put(url, {'bd_id': self.other_bd_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify application was updated
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.other_bd_user)
        
        # Verify notification was created for the new BD
        self.assertTrue(Notification.objects.filter(
            user=self.other_bd_user,
            notification_type='application_status'
        ).exists())
        
        # Verify note was created about the reassignment
        self.assertTrue(Note.objects.filter(
            application=self.application,
            content__contains="BD reassigned from"
        ).exists())

    def test_update_bd_assignment_without_existing_bd(self):
        """Test updating a BD assignment when no BD is assigned"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        # Try to update when no BD is assigned
        response = self.client.put(url, {'bd_id': self.bd_user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no assignment was made
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)

    def test_update_bd_assignment_with_same_bd(self):
        """Test updating a BD assignment with the same BD"""
        # First assign a BD
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        # Try to update with the same BD
        response = self.client.put(url, {'bd_id': self.bd_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "BD assignment unchanged")
        
        # Verify assignment didn't change
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)

    def test_remove_bd_assignment(self):
        """Test removing a BD assignment with DELETE method"""
        # First assign a BD
        self.application.assigned_bd = self.bd_user
        self.application.save()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        # Now remove the assignment
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify assignment was removed
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)
        
        # Verify note was created about the removal
        self.assertTrue(Note.objects.filter(
            application=self.application,
            content__contains="BD assignment removed"
        ).exists())

    def test_remove_bd_assignment_without_existing_bd(self):
        """Test removing a BD assignment when no BD is assigned"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        # Try to remove when no BD is assigned
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_invalid_bd(self):
        """Test assigning an invalid BD ID"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        response = self.client.post(url, {'bd_id': 99999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no assignment was made
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)

    def test_assign_non_bd_user(self):
        """Test assigning a user who is not a BD"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-assign-bd', kwargs={'pk': self.application.pk})
        
        response = self.client.post(url, {'bd_id': self.regular_user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify no assignment was made
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)

    def test_bd_claim_application(self):
        """Test BD claiming an unassigned application"""
        self.client.force_authenticate(user=self.bd_user)
        url = reverse('bdm-claim-application')
        
        response = self.client.post(url, {'application_id': self.application.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify application was assigned
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.bd_user)
        
        # Verify notification was created
        self.assertTrue(Notification.objects.filter(
            user=self.bd_user,
            notification_type='application_status'
        ).exists())
        
        # Verify note was created
        self.assertTrue(Note.objects.filter(
            application=self.application,
            created_by=self.bd_user
        ).exists())

    def test_bd_claim_already_assigned_application(self):
        """Test BD trying to claim an already assigned application"""
        self.application.assigned_bd = self.other_bd_user
        self.application.save()
        
        self.client.force_authenticate(user=self.bd_user)
        url = reverse('bdm-claim-application')
        
        response = self.client.post(url, {'application_id': self.application.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify assignment didn't change
        self.application.refresh_from_db()
        self.assertEqual(self.application.assigned_bd, self.other_bd_user)

    def test_non_bd_claim_application(self):
        """Test non-BD user trying to claim an application"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('bdm-claim-application')
        
        response = self.client.post(url, {'application_id': self.application.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify no assignment was made
        self.application.refresh_from_db()
        self.assertIsNone(self.application.assigned_bd)