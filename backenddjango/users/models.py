from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import UserManager


class User(AbstractUser):
    """
    Custom User model with role-based permissions
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('broker', 'Broker'),
        ('bd', 'Business Development'),
        ('client', 'Client'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True, default='')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email


class Notification(models.Model):
    """
    Model for user notifications
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('application_status', 'Application Status Change'),
        ('repayment_upcoming', 'Repayment Upcoming'),
        ('repayment_overdue', 'Repayment Overdue'),
        ('note_reminder', 'Note Reminder'),
        ('document_uploaded', 'Document Uploaded'),
        ('signature_required', 'Signature Required'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"
    
    def mark_as_read(self):
        """
        Mark the notification as read
        """
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class NotificationPreference(models.Model):
    """
    Model for user notification preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # In-app notification preferences
    application_status_in_app = models.BooleanField(default=True)
    repayment_upcoming_in_app = models.BooleanField(default=True)
    repayment_overdue_in_app = models.BooleanField(default=True)
    note_reminder_in_app = models.BooleanField(default=True)
    document_uploaded_in_app = models.BooleanField(default=True)
    signature_required_in_app = models.BooleanField(default=True)
    system_in_app = models.BooleanField(default=True)
    
    # Email notification preferences
    application_status_email = models.BooleanField(default=True)
    repayment_upcoming_email = models.BooleanField(default=True)
    repayment_overdue_email = models.BooleanField(default=True)
    note_reminder_email = models.BooleanField(default=True)
    document_uploaded_email = models.BooleanField(default=False)
    signature_required_email = models.BooleanField(default=True)
    system_email = models.BooleanField(default=False)
    
    # Email digest preferences
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification Preferences for {self.user.email}"
    
    def get_in_app_preference(self, notification_type):
        """
        Get in-app notification preference for a specific notification type
        """
        preference_map = {
            'application_status': self.application_status_in_app,
            'repayment_upcoming': self.repayment_upcoming_in_app,
            'repayment_overdue': self.repayment_overdue_in_app,
            'note_reminder': self.note_reminder_in_app,
            'document_uploaded': self.document_uploaded_in_app,
            'signature_required': self.signature_required_in_app,
            'system': self.system_in_app,
        }
        return preference_map.get(notification_type, True)
    
    def get_email_preference(self, notification_type):
        """
        Get email notification preference for a specific notification type
        """
        preference_map = {
            'application_status': self.application_status_email,
            'repayment_upcoming': self.repayment_upcoming_email,
            'repayment_overdue': self.repayment_overdue_email,
            'note_reminder': self.note_reminder_email,
            'document_uploaded': self.document_uploaded_email,
            'signature_required': self.signature_required_email,
            'system': self.system_email,
        }
        return preference_map.get(notification_type, False)
