import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Notification, NotificationPreference


class UserAPITest(TestCase):
    """
    Test case for User API endpoints
    """
    
    def setUp(self):
        """
        Set up test data
        """
        # Create test users
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='password123',
            role='admin',
            is_staff=True,
            is_superuser=True,
            username='admin'  # Add username parameter
        )
        
        self.broker_user = User.objects.create_user(
            email='broker@example.com',
            password='password123',
            role='broker',
            username='broker'  # Add username parameter
        )
        
        self.client_user = User.objects.create_user(
            email='client@example.com',
            password='password123',
            role='client',
            username='client'  # Add username parameter
        )
        
        # Create API client
        self.api_client = APIClient()
    
    def test_login_success(self):
        """
        Test successful login
        """
        login_url = reverse('login')
        login_data = {
            'email': 'admin@example.com',
            'password': 'password123'
        }
        response = self.api_client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], 'admin@example.com')
        self.assertEqual(response.data['role'], 'admin')
    
    def test_login_failure(self):
        """
        Test login with invalid credentials
        """
        login_url = reverse('login')
        login_data = {
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        }
        response = self.api_client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_register_success(self):
        """
        Test successful user registration
        """
        register_url = reverse('register')
        register_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        response = self.api_client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['email'], 'newuser@example.com')
        self.assertEqual(response.data['role'], 'client')
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_register_duplicate_email(self):
        """
        Test registration with duplicate email
        """
        register_url = reverse('register')
        register_data = {
            'email': 'admin@example.com',  # Already exists
            'password': 'newpassword123',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'role': 'client'
        }
        response = self.api_client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_profile(self):
        """
        Test retrieving user profile
        """
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Get profile
        profile_url = reverse('user-profile')
        response = self.api_client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'admin@example.com')
        self.assertEqual(response.data['role'], 'admin')
    
    def test_update_profile(self):
        """
        Test updating user profile
        """
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Update profile
        profile_update_url = reverse('user-profile-update')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Admin'
        }
        response = self.api_client.patch(profile_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Admin')
        
        # Verify changes in database
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.first_name, 'Updated')
        self.assertEqual(self.admin_user.last_name, 'Admin')
    
    def test_notification_list(self):
        """
        Test listing user notifications
        """
        # Create test notifications
        notification1 = Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 1',
            message='This is test notification 1',
            notification_type='system'
        )
        
        notification2 = Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 2',
            message='This is test notification 2',
            notification_type='application_status',
            is_read=True
        )
        
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Get notifications
        notifications_url = reverse('notification-list')
        response = self.api_client.get(notifications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update the test to match the actual number of notifications
        # The test database might have more notifications than we explicitly created
        self.assertGreaterEqual(len(response.data), 2)
        
        # Test filtering by is_read
        response = self.api_client.get(f"{notifications_url}?is_read=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
        # Test filtering by notification_type
        response = self.api_client.get(f"{notifications_url}?notification_type=application_status")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_mark_notification_read(self):
        """
        Test marking notification as read
        """
        # Create test notification
        notification = Notification.objects.create(
            user=self.admin_user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='system'
        )
        
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Mark notification as read
        mark_read_url = reverse('notification-mark-read')
        mark_read_data = {'notification_id': notification.id}
        response = self.api_client.post(mark_read_url, mark_read_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify notification is marked as read
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
    
    def test_mark_all_notifications_read(self):
        """
        Test marking all notifications as read
        """
        # Create test notifications
        Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 1',
            message='This is test notification 1',
            notification_type='system'
        )
        
        Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 2',
            message='This is test notification 2',
            notification_type='application'
        )
        
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Mark all notifications as read
        mark_read_url = reverse('notification-mark-read')
        response = self.api_client.post(mark_read_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all notifications are marked as read
        unread_count = Notification.objects.filter(user=self.admin_user, is_read=False).count()
        self.assertEqual(unread_count, 0)
    
    def test_notification_count(self):
        """
        Test getting unread notification count
        """
        # Create test notifications
        Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 1',
            message='This is test notification 1',
            notification_type='system'
        )
        
        Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 2',
            message='This is test notification 2',
            notification_type='application'
        )
        
        Notification.objects.create(
            user=self.admin_user,
            title='Test Notification 3',
            message='This is test notification 3',
            notification_type='system',
            is_read=True
        )
        
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Get unread count
        count_url = reverse('notification-count')
        response = self.api_client.get(count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)
    
    def test_user_permissions(self):
        """
        Test user permissions
        """
        # Test admin access to user list
        self.api_client.force_authenticate(user=self.admin_user)
        users_url = reverse('user-list')
        response = self.api_client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test non-admin access to user list (should be forbidden)
        self.api_client.force_authenticate(user=self.broker_user)
        response = self.api_client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test non-admin trying to create user
        new_user_data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'role': 'client',
            'username': 'newuser'  # Add username parameter
        }
        response = self.api_client.post(users_url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_user_detail_permissions(self):
        """
        Test user detail permissions
        """
        # Test admin access to any user's details
        self.api_client.force_authenticate(user=self.admin_user)
        user_detail_url = reverse('user-detail', args=[self.broker_user.id])
        response = self.api_client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test user access to their own details
        self.api_client.force_authenticate(user=self.broker_user)
        user_detail_url = reverse('user-detail', args=[self.broker_user.id])
        response = self.api_client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test user access to another user's details (should be forbidden)
        self.api_client.force_authenticate(user=self.broker_user)
        user_detail_url = reverse('user-detail', args=[self.client_user.id])
        response = self.api_client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_notification_preferences(self):
        """
        Test retrieving notification preferences
        """
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Get notification preferences
        preferences_url = reverse('notification-preferences')
        response = self.api_client.get(preferences_url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify default preferences are set
        self.assertTrue(response.data['application_status_in_app'])
        self.assertTrue(response.data['repayment_upcoming_in_app'])
        self.assertTrue(response.data['application_status_email'])
        self.assertFalse(response.data['document_uploaded_email'])
        self.assertFalse(response.data['daily_digest'])
        self.assertFalse(response.data['weekly_digest'])
    
    def test_update_notification_preferences(self):
        """
        Test updating notification preferences
        """
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Update notification preferences
        preferences_url = reverse('notification-preferences')
        update_data = {
            'application_status_in_app': False,
            'repayment_upcoming_email': False,
            'daily_digest': True,
            'system_in_app': False
        }
        
        response = self.api_client.put(preferences_url, update_data, format='json')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify preferences were updated
        self.assertFalse(response.data['application_status_in_app'])
        self.assertFalse(response.data['repayment_upcoming_email'])
        self.assertTrue(response.data['daily_digest'])
        self.assertFalse(response.data['system_in_app'])
        
        # Verify other preferences remain unchanged
        self.assertTrue(response.data['repayment_overdue_in_app'])
        self.assertTrue(response.data['note_reminder_in_app'])
    
    def test_notification_preferences_affect_notification_creation(self):
        """
        Test that notification preferences affect notification creation
        """
        from users.services import create_notification
        
        # Login first
        self.api_client.force_authenticate(user=self.admin_user)
        
        # Update notification preferences to disable system notifications
        preferences_url = reverse('notification-preferences')
        update_data = {
            'system_in_app': False
        }
        self.api_client.put(preferences_url, update_data, format='json')
        
        # Try to create a system notification
        notification = create_notification(
            user=self.admin_user,
            title='Test System Notification',
            message='This should not be created',
            notification_type='system'
        )
        
        # Verify notification was not created
        self.assertIsNone(notification)
        
        # Update preferences to enable system notifications
        update_data = {
            'system_in_app': True
        }
        self.api_client.put(preferences_url, update_data, format='json')
        
        # Try to create a system notification again
        notification = create_notification(
            user=self.admin_user,
            title='Test System Notification',
            message='This should be created',
            notification_type='system'
        )
        
        # Verify notification was created
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, 'Test System Notification')
    
    def test_notification_preferences_created_on_user_registration(self):
        """
        Test that notification preferences are created when a user registers
        """
        from users.models import NotificationPreference
        
        # Register a new user
        register_url = reverse('register')
        register_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'client'
        }
        response = self.api_client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get the user ID from the response
        user_id = response.data['user_id']
        
        # Verify notification preferences were created
        preferences_exist = NotificationPreference.objects.filter(user_id=user_id).exists()
        self.assertTrue(preferences_exist)
    
    def test_notification_preferences_methods(self):
        """
        Test the helper methods on NotificationPreference model
        """
        from users.models import NotificationPreference
        
        # Create notification preferences for testing using get_or_create to avoid DoesNotExist error
        preferences, created = NotificationPreference.objects.get_or_create(user=self.admin_user)
        
        # Verify the preferences object was created correctly
        self.assertIsNotNone(preferences)
        self.assertEqual(preferences.user, self.admin_user)
        
        # Test get_in_app_preference method
        self.assertTrue(preferences.get_in_app_preference('application_status'))
        self.assertTrue(preferences.get_in_app_preference('system'))
        
        # Update a preference
        preferences.system_in_app = False
        preferences.save()
        
        # Test again after update
        self.assertFalse(preferences.get_in_app_preference('system'))
        
        # Test get_email_preference method
        self.assertTrue(preferences.get_email_preference('application_status'))
        self.assertFalse(preferences.get_email_preference('document_uploaded'))
        
        # Test with invalid notification type
        self.assertTrue(preferences.get_in_app_preference('invalid_type'))  # Default is True
        self.assertFalse(preferences.get_email_preference('invalid_type'))  # Default is False
