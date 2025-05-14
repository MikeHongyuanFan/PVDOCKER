from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import Application
from documents.models import Note, Repayment
from users.services import create_notification


@shared_task
def check_stagnant_applications():
    """
    Check for applications that haven't had their stage updated in X days
    and notify the BD
    """
    # Define the threshold for stagnant applications (e.g., 14 days)
    threshold_days = 14
    threshold_date = timezone.now() - timedelta(days=threshold_days)
    
    # Find applications that haven't had their stage updated in threshold_days
    stagnant_applications = Application.objects.filter(
        stage_last_updated__lt=threshold_date
    ).exclude(
        stage__in=['funded', 'declined', 'withdrawn']
    )
    
    for application in stagnant_applications:
        if application.bd and application.bd.user:
            # Create system notification
            notification_title = f'Stagnant Application Alert: {application.reference_number}'
            notification_message = f'''
            Application {application.reference_number} has been in the {application.get_stage_display()} stage for over {threshold_days} days.
            
            Please review this application and update its status or contact the broker.
            
            Application Details:
            - Reference: {application.reference_number}
            - Stage: {application.get_stage_display()}
            - Loan Amount: ${application.loan_amount}
            - Broker: {application.broker.name if application.broker else 'N/A'}
            - Last Stage Update: {application.stage_last_updated.strftime('%d/%m/%Y')}
            '''
            
            # Create notification for the BD
            create_notification(
                user=application.bd.user,
                title=notification_title,
                message=notification_message,
                notification_type='system',
                related_object_id=application.id,
                related_object_type='application'
            )


@shared_task
def check_stale_applications():
    """
    Check for applications that haven't changed stage in X days
    and notify the BD
    """
    # Define the threshold for stale applications (e.g., 14 days)
    threshold_days = 14
    threshold_date = timezone.now() - timedelta(days=threshold_days)
    
    # Find applications that haven't been updated in threshold_days
    stale_applications = Application.objects.filter(
        updated_at__lt=threshold_date
    ).exclude(
        stage__in=['funded', 'declined', 'withdrawn']
    )
    
    for application in stale_applications:
        if application.bd and application.bd.user and application.bd.user.email:
            # Send email notification
            send_mail(
                subject=f'Stale Application Alert: {application.reference_number}',
                message=f'''
                Application {application.reference_number} has been in the {application.get_stage_display()} stage for over {threshold_days} days.
                
                Please review this application and update its status or contact the broker.
                
                Application Details:
                - Reference: {application.reference_number}
                - Stage: {application.get_stage_display()}
                - Loan Amount: ${application.loan_amount}
                - Broker: {application.broker.name if application.broker else 'N/A'}
                - Last Updated: {application.updated_at.strftime('%d/%m/%Y')}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.bd.user.email],
                fail_silently=True,
            )


@shared_task
def check_note_reminders():
    """
    Check for notes with remind_date today and send notifications
    """
    today = timezone.now().date()
    
    # Find notes with remind_date today
    reminder_notes = Note.objects.filter(
        remind_date__date=today
    )
    
    for note in reminder_notes:
        # Determine recipients
        recipients = []
        
        # Add note creator
        if note.created_by and note.created_by.email:
            recipients.append(note.created_by.email)
        
        # Add application BD if exists
        if note.application and note.application.bd and note.application.bd.user and note.application.bd.user.email:
            recipients.append(note.application.bd.user.email)
        
        # Send email if we have recipients
        if recipients:
            send_mail(
                subject=f'Note Reminder: {note.title}',
                message=f'''
                This is a reminder for the note: {note.title}
                
                Content: {note.content}
                
                Related to Application: {note.application.reference_number if note.application else 'N/A'}
                Related to Borrower: {note.borrower if note.borrower else 'N/A'}
                
                Created on: {note.created_at.strftime('%d/%m/%Y')}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=True,
            )


@shared_task
def check_repayment_reminders():
    """
    Check for upcoming and overdue repayments and send notifications
    """
    today = timezone.now().date()
    
    # Upcoming repayments (7 days before due date)
    upcoming_date = today + timedelta(days=7)
    upcoming_repayments = Repayment.objects.filter(
        due_date=upcoming_date,
        paid_date__isnull=True,
        reminder_sent=False
    )
    
    for repayment in upcoming_repayments:
        # Notify borrowers
        borrowers = repayment.application.borrowers.all()
        for borrower in borrowers:
            if hasattr(borrower, 'user') and borrower.user and borrower.user.email:
                send_mail(
                    subject=f'Upcoming Repayment Reminder',
                    message=f'''
                    This is a reminder that you have a repayment of ${repayment.amount} due on {repayment.due_date.strftime('%d/%m/%Y')}.
                    
                    Application Reference: {repayment.application.reference_number}
                    
                    Please ensure funds are available in your account for this repayment.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[borrower.user.email],
                    fail_silently=True,
                )
        
        # Mark as reminded
        repayment.reminder_sent = True
        repayment.save()
    
    # 3 days overdue - notify borrowers
    overdue_3_date = today - timedelta(days=3)
    overdue_3_repayments = Repayment.objects.filter(
        due_date=overdue_3_date,
        paid_date__isnull=True,
        overdue_3_day_sent=False
    )
    
    for repayment in overdue_3_repayments:
        # Notify borrowers
        borrowers = repayment.application.borrowers.all()
        for borrower in borrowers:
            if hasattr(borrower, 'user') and borrower.user and borrower.user.email:
                send_mail(
                    subject=f'OVERDUE Repayment Notice',
                    message=f'''
                    IMPORTANT: Your repayment of ${repayment.amount} was due on {repayment.due_date.strftime('%d/%m/%Y')} and is now 3 days overdue.
                    
                    Application Reference: {repayment.application.reference_number}
                    
                    Please make this payment immediately to avoid additional fees and penalties.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[borrower.user.email],
                    fail_silently=True,
                )
        
        # Mark as notified
        repayment.overdue_3_day_sent = True
        repayment.save()
    
    # 7 days overdue - notify borrowers again
    overdue_7_date = today - timedelta(days=7)
    overdue_7_repayments = Repayment.objects.filter(
        due_date=overdue_7_date,
        paid_date__isnull=True,
        overdue_7_day_sent=False
    )
    
    for repayment in overdue_7_repayments:
        # Notify borrowers
        borrowers = repayment.application.borrowers.all()
        for borrower in borrowers:
            if hasattr(borrower, 'user') and borrower.user and borrower.user.email:
                send_mail(
                    subject=f'URGENT: 7 Days OVERDUE Repayment',
                    message=f'''
                    URGENT: Your repayment of ${repayment.amount} was due on {repayment.due_date.strftime('%d/%m/%Y')} and is now 7 days overdue.
                    
                    Application Reference: {repayment.application.reference_number}
                    
                    This is your final notice before this matter is escalated. Please make this payment immediately.
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[borrower.user.email],
                    fail_silently=True,
                )
        
        # Mark as notified
        repayment.overdue_7_day_sent = True
        repayment.save()
    
    # 10 days overdue - notify BD
    overdue_10_date = today - timedelta(days=10)
    overdue_10_repayments = Repayment.objects.filter(
        due_date=overdue_10_date,
        paid_date__isnull=True,
        overdue_10_day_sent=False
    )
    
    for repayment in overdue_10_repayments:
        # Notify BD
        if repayment.application.bd and repayment.application.bd.user and repayment.application.bd.user.email:
            borrowers_list = ", ".join([str(b) for b in repayment.application.borrowers.all()])
            
            send_mail(
                subject=f'ESCALATION: 10 Days Overdue Repayment',
                message=f'''
                A repayment of ${repayment.amount} for application {repayment.application.reference_number} is now 10 days overdue.
                
                Borrowers: {borrowers_list}
                Due Date: {repayment.due_date.strftime('%d/%m/%Y')}
                
                This matter has been escalated to you for further action.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[repayment.application.bd.user.email],
                fail_silently=True,
            )
        
        # Mark as notified
        repayment.overdue_10_day_sent = True
        repayment.save()