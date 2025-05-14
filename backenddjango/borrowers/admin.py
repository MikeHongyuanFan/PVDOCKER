from django.contrib import admin
from .models import Borrower, Director, Asset, Liability, Guarantor

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'email', 'phone', 'is_company', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('is_company', 'created_at', 'residency_status', 'employment_type')
    raw_id_fields = ('user', 'created_by')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'marital_status', 'residency_status')
        }),
        ('Address Information', {
            'fields': ('residential_address', 'mailing_address')
        }),
        ('Employment Information', {
            'fields': ('employment_type', 'employer_name', 'employer_address', 'job_title', 'employment_duration')
        }),
        ('Financial Information', {
            'fields': ('annual_income', 'other_income', 'monthly_expenses')
        }),
        ('Bank Account Information', {
            'fields': ('bank_name', 'bank_account_name', 'bank_account_number', 'bank_bsb')
        }),
        ('Company Information', {
            'fields': ('is_company', 'company_name', 'company_abn', 'company_acn', 'industry_type', 'contact_number', 
                      'annual_company_income', 'is_trustee', 'is_smsf_trustee', 'trustee_name')
        }),
        ('Registered Address', {
            'fields': ('registered_address_unit', 'registered_address_street_no', 'registered_address_street_name',
                      'registered_address_suburb', 'registered_address_state', 'registered_address_postcode')
        }),
        ('Additional Information', {
            'fields': ('referral_source', 'tags', 'notes_text')
        }),
        ('System Information', {
            'fields': ('user', 'created_by')
        }),
    )
    
    def get_name(self, obj):
        if obj.is_company:
            return obj.company_name
        return f"{obj.first_name} {obj.last_name}"
    get_name.short_description = 'Name'

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'borrower', 'roles', 'created_at')
    search_fields = ('name', 'roles', 'borrower__company_name')
    list_filter = ('created_at',)
    raw_id_fields = ('borrower', 'created_by')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'created_at')
    search_fields = ('description', 'address')
    list_filter = ('asset_type', 'to_be_refinanced', 'created_at')
    raw_id_fields = ('borrower', 'guarantor', 'created_by')

@admin.register(Liability)
class LiabilityAdmin(admin.ModelAdmin):
    list_display = ('liability_type', 'description', 'amount', 'lender', 'monthly_payment', 'to_be_refinanced', 'created_at')
    search_fields = ('description', 'lender')
    list_filter = ('liability_type', 'to_be_refinanced', 'created_at')
    raw_id_fields = ('borrower', 'guarantor', 'created_by')

@admin.register(Guarantor)
class GuarantorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'guarantor_type', 'email', 'mobile', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company_name')
    list_filter = ('guarantor_type', 'created_at')
    raw_id_fields = ('borrower', 'application', 'created_by')
    fieldsets = (
        ('Basic Information', {
            'fields': ('guarantor_type', 'title', 'first_name', 'last_name', 'date_of_birth', 'drivers_licence_no', 
                      'home_phone', 'mobile', 'email')
        }),
        ('Address Information', {
            'fields': ('address_unit', 'address_street_no', 'address_street_name', 'address_suburb', 
                      'address_state', 'address_postcode', 'address')
        }),
        ('Employment Information', {
            'fields': ('occupation', 'employer_name', 'employment_type', 'annual_income')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_abn', 'company_acn')
        }),
        ('Relationships', {
            'fields': ('borrower', 'application')
        }),
        ('System Information', {
            'fields': ('created_by',)
        }),
    )
    
    def get_name(self, obj):
        if obj.guarantor_type == 'company':
            return obj.company_name
        return f"{obj.first_name} {obj.last_name}"
    get_name.short_description = 'Name'
