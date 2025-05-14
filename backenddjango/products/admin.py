from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_applications_count', 'get_documents_count', 'get_borrowers_count', 'created_at', 'updated_at')
    search_fields = ('name',)
    filter_horizontal = ('applications', 'documents', 'borrowers')
    raw_id_fields = ('created_by',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('name',)
        }),
        ('Relationships', {
            'fields': ('applications', 'documents', 'borrowers')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    get_applications_count.short_description = 'Applications'
    
    def get_documents_count(self, obj):
        return obj.documents.count()
    get_documents_count.short_description = 'Documents'
    
    def get_borrowers_count(self, obj):
        return obj.borrowers.count()
    get_borrowers_count.short_description = 'Borrowers'