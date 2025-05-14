from django.db import models
from django.conf import settings


class Reminder(models.Model):
    """
    Model for email reminders
    """
    RECIPIENT_TYPE_CHOICES = [
        ('client', 'Client'),
        ('bdm', 'Business Development Manager'),
        ('broker', 'Broker'),
        ('custom', 'Custom Email'),
    ]
    
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES)
    recipient_email = models.EmailField()
    send_datetime = models.DateTimeField()
    email_body = models.TextField()
    subject = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_reminders')
    send_as_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='send_as_reminders', null=True, blank=True)
    reply_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='reply_to_reminders', null=True, blank=True)
    
    # Status fields
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    # Optional related objects
    related_application = models.ForeignKey('applications.Application', on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders')
    related_borrower = models.ForeignKey('borrowers.Borrower', on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['send_datetime']
        
    def __str__(self):
        return f"Reminder: {self.subject} (to: {self.recipient_email})"