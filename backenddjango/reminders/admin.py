from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient_email', 'recipient_type', 'send_datetime', 'is_sent')
    list_filter = ('recipient_type', 'is_sent', 'send_datetime')
    search_fields = ('subject', 'recipient_email', 'email_body')
    date_hierarchy = 'send_datetime'
    readonly_fields = ('sent_at', 'error_message')