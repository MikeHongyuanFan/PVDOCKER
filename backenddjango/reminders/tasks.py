from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Reminder


@shared_task
def check_due_reminders():
    """
    Check for reminders that are due to be sent and send them
    """
    now = timezone.now()
    
    # Find reminders that are due but not yet sent
    due_reminders = Reminder.objects.filter(
        send_datetime__lte=now,
        is_sent=False
    )
    
    for reminder in due_reminders:
        try:
            # Create email message
            email = EmailMessage(
                subject=reminder.subject,
                body=reminder.email_body,
                to=[reminder.recipient_email],
            )
            
            # Set custom From header if send_as_user is specified
            if reminder.send_as_user and reminder.send_as_user.email:
                # Format: "User Name <user@example.com>"
                from_email = f'"{reminder.send_as_user.get_full_name()}" <{reminder.send_as_user.email}>'
                email.from_email = from_email
            else:
                email.from_email = settings.DEFAULT_FROM_EMAIL
            
            # Set Reply-To header if specified
            if reminder.reply_to_user and reminder.reply_to_user.email:
                email.reply_to = [reminder.reply_to_user.email]
            
            # Send email
            email.send(fail_silently=False)
            
            # Update reminder status
            reminder.is_sent = True
            reminder.sent_at = timezone.now()
            reminder.save()
            
        except Exception as e:
            # Log error and update reminder
            reminder.error_message = str(e)
            reminder.save()
            
            # Re-raise for Celery to handle
            raise