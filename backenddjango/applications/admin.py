from django.contrib import admin
from .models import Application, SecurityProperty, LoanRequirement, Document, Fee, Repayment, FundingCalculationHistory


class SecurityPropertyInline(admin.TabularInline):
    model = SecurityProperty
    extra = 0


class LoanRequirementInline(admin.TabularInline):
    model = LoanRequirement
    extra = 0


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0


class RepaymentInline(admin.TabularInline):
    model = Repayment
    extra = 0


class FundingCalculationHistoryInline(admin.TabularInline):
    model = FundingCalculationHistory
    extra = 0
    readonly_fields = ('created_at', 'created_by')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'stage', 'loan_amount', 'created_at', 'updated_at')
    list_filter = ('stage', 'application_type', 'loan_purpose')
    search_fields = ('reference_number', 'purpose', 'security_address')
    readonly_fields = ('reference_number', 'created_at', 'updated_at', 'stage_last_updated')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('reference_number', 'stage', 'stage_last_updated', 'application_type', 'purpose')
        }),
        ('Loan Details', {
            'fields': ('loan_amount', 'loan_term', 'interest_rate', 'repayment_frequency', 
                      'product_id', 'estimated_settlement_date')
        }),
        ('Loan Purpose', {
            'fields': ('loan_purpose', 'additional_comments', 'prior_application', 'prior_application_details')
        }),
        ('Exit Strategy', {
            'fields': ('exit_strategy', 'exit_strategy_details')
        }),
        ('General Solvency Enquiries', {
            'fields': ('has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
                      'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
                      'has_payment_arrangements', 'solvency_enquiries_details')
        }),
        ('Relationships', {
            'fields': ('broker', 'branch', 'bd', 'borrowers', 'guarantors')
        }),
        ('Security Property (Legacy)', {
            'fields': ('security_address', 'security_type', 'security_value')
        }),
        ('Valuer Information', {
            'fields': ('valuer_company_name', 'valuer_contact_name', 'valuer_phone', 'valuer_email',
                      'valuation_date', 'valuation_amount')
        }),
        ('Quantity Surveyor Information', {
            'fields': ('qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email', 'qs_report_date')
        }),
        ('Signature and Document', {
            'fields': ('signed_by', 'signature_date', 'uploaded_pdf_path')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    inlines = [
        SecurityPropertyInline,
        LoanRequirementInline,
        DocumentInline,
        FeeInline,
        RepaymentInline,
        FundingCalculationHistoryInline,
    ]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SecurityProperty)
class SecurityPropertyAdmin(admin.ModelAdmin):
    list_display = ('get_address', 'property_type', 'estimated_value', 'application')
    list_filter = ('property_type', 'occupancy')
    search_fields = ('address_street_name', 'address_suburb', 'address_postcode')
    
    def get_address(self, obj):
        address_parts = [
            obj.address_unit,
            obj.address_street_no,
            obj.address_street_name,
            obj.address_suburb,
            obj.address_state,
            obj.address_postcode
        ]
        return ' '.join(filter(None, address_parts))
    get_address.short_description = 'Address'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'description', 'application', 'uploaded_at', 'uploaded_by')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('description',)
    date_hierarchy = 'uploaded_at'


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_type', 'amount', 'due_date', 'status', 'application')
    list_filter = ('fee_type', 'status', 'due_date')
    search_fields = ('notes',)
    date_hierarchy = 'due_date'


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('due_date', 'amount', 'status', 'paid_date', 'application')
    list_filter = ('status', 'due_date', 'paid_date')
    search_fields = ('notes',)
    date_hierarchy = 'due_date'


@admin.register(FundingCalculationHistory)
class FundingCalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('application', 'created_by', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'created_by')
    date_hierarchy = 'created_at'
