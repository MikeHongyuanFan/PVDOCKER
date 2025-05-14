import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')

app = Celery('crm_backend')

# Use a string here to avoid namespace issues
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'check-stale-applications': {
        'task': 'applications.tasks.check_stale_applications',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9 AM
    },
    'check-stagnant-applications': {
        'task': 'applications.tasks.check_stagnant_applications',
        'schedule': crontab(hour=10, minute=0),  # Run daily at 10 AM
    },
    'check-note-reminders': {
        'task': 'applications.tasks.check_note_reminders',
        'schedule': crontab(hour=8, minute=0),  # Run daily at 8 AM
    },
    'check-repayment-reminders': {
        'task': 'applications.tasks.check_repayment_reminders',
        'schedule': crontab(hour=7, minute=0),  # Run daily at 7 AM
    },
    'check-due-reminders': {
        'task': 'reminders.tasks.check_due_reminders',
        'schedule': crontab(minute=0),  # Run hourly at the start of each hour
    },
}
