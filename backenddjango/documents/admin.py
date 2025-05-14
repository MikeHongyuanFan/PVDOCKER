from django.contrib import admin
from .models import Document, Note, Fee, Repayment, Ledger, NoteComment

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'file_name', 'application', 'borrower', 'version', 'created_at')
    list_filter = ('document_type', 'created_at', 'version')
    search_fields = ('title', 'description', 'file_name', 'application__reference_number')
    raw_id_fields = ('application', 'borrower', 'previous_version', 'created_by')
    readonly_fields = ('file_size', 'file_type', 'created_at', 'updated_at')
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'description', 'document_type', 'file')
        }),
        ('File Details', {
            'fields': ('file_name', 'file_size', 'file_type')
        }),
        ('Versioning', {
            'fields': ('version', 'previous_version')
        }),
        ('Relationships', {
            'fields': ('application', 'borrower')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'application', 'borrower', 'assigned_to', 'remind_date', 'created_at')
    list_filter = ('created_at', 'remind_date')
    search_fields = ('title', 'content', 'application__reference_number')
    raw_id_fields = ('application', 'borrower', 'assigned_to', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'content', 'remind_date')
        }),
        ('Relationships', {
            'fields': ('application', 'borrower')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'amount', 'due_date', 'paid_date', 'application', 'created_at')
    list_filter = ('fee_type', 'due_date', 'paid_date', 'created_at')
    search_fields = ('description', 'application__reference_number')
    raw_id_fields = ('application', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Fee Information', {
            'fields': ('fee_type', 'description', 'amount', 'due_date', 'paid_date', 'invoice')
        }),
        ('Relationships', {
            'fields': ('application',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'due_date', 'paid_date', 'application', 'created_at')
    list_filter = ('due_date', 'paid_date', 'created_at', 'reminder_sent', 'overdue_3_day_sent', 'overdue_7_day_sent', 'overdue_10_day_sent')
    search_fields = ('application__reference_number',)
    raw_id_fields = ('application', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Repayment Information', {
            'fields': ('amount', 'due_date', 'paid_date', 'invoice')
        }),
        ('Relationships', {
            'fields': ('application',)
        }),
        ('Notification Status', {
            'fields': ('reminder_sent', 'overdue_3_day_sent', 'overdue_7_day_sent', 'overdue_10_day_sent')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'transaction_date', 'application', 'created_at')
    list_filter = ('transaction_type', 'transaction_date', 'created_at')
    search_fields = ('description', 'application__reference_number')
    raw_id_fields = ('application', 'related_fee', 'related_repayment', 'created_by')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_type', 'amount', 'description', 'transaction_date')
        }),
        ('Relationships', {
            'fields': ('application', 'related_fee', 'related_repayment')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at')
        }),
    )

@admin.register(NoteComment)
class NoteCommentAdmin(admin.ModelAdmin):
    list_display = ('note', 'content_preview', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'note__title')
    raw_id_fields = ('note', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = 'Content'
