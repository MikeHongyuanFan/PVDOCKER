import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail
from users.models import User


@pytest.mark.django_db
class TestPasswordReset:
    """
    Tests for password reset functionality
    """
    
    def test_password_reset_request(self, client):
        """
        Test requesting a password reset
        """
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            password='oldpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Request password reset
        url = reverse('reset-password-request')
        response = client.post(url, {'email': 'test@example.com'})
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Password reset email has been sent.'
        
        # Check that an email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Password Reset Request'
        assert 'test@example.com' in mail.outbox[0].to
        
        # Check that the email contains the reset URL with uid and token
        email_body = mail.outbox[0].body
        assert '/reset-password-confirm/' in email_body
        assert 'uid=' in email_body
        assert 'token=' in email_body
    
    def test_password_reset_request_nonexistent_email(self, client):
        """
        Test requesting a password reset for a non-existent email
        """
        # Request password reset for non-existent email
        url = reverse('reset-password-request')
        response = client.post(url, {'email': 'nonexistent@example.com'})
        
        # Check response (should still be 200 for security reasons)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Password reset email has been sent.'
        
        # Check that no email was sent
        assert len(mail.outbox) == 0
    
    def test_password_reset_confirm(self, client):
        """
        Test confirming a password reset
        """
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            password='oldpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Generate token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Confirm password reset
        url = reverse('reset-password-confirm')
        response = client.post(url, {
            'uid': uid,
            'token': token,
            'new_password': 'newpassword123'
        })
        
        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Password has been reset successfully.'
        
        # Check that the password was changed
        user.refresh_from_db()
        assert user.check_password('newpassword123')
    
    def test_password_reset_confirm_invalid_token(self, client):
        """
        Test confirming a password reset with an invalid token
        """
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            password='oldpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Generate uid but use invalid token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Confirm password reset with invalid token
        url = reverse('reset-password-confirm')
        response = client.post(url, {
            'uid': uid,
            'token': 'invalid-token',
            'new_password': 'newpassword123'
        })
        
        # Check response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Invalid token' in response.data['error']
        
        # Check that the password was not changed
        user.refresh_from_db()
        assert user.check_password('oldpassword123')
    
    def test_password_reset_confirm_invalid_uid(self, client):
        """
        Test confirming a password reset with an invalid uid
        """
        # Create a user
        user = User.objects.create_user(
            email='test@example.com',
            password='oldpassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Generate token but use invalid uid
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        
        # Confirm password reset with invalid uid
        url = reverse('reset-password-confirm')
        response = client.post(url, {
            'uid': 'invalid-uid',
            'token': token,
            'new_password': 'newpassword123'
        })
        
        # Check response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Invalid reset link' in response.data['error']
        
        # Check that the password was not changed
        user.refresh_from_db()
        assert user.check_password('oldpassword123')