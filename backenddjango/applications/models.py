from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models import JSONField
from brokers.models import Broker, Branch, BDM


def generate_reference_number():
    """Generate a unique reference number for applications"""
    prefix = "APP"
    random_suffix = get_random_string(length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return f"{prefix}-{random_suffix}"


class Application(models.Model):
    """
    Model for loan applications
    """
    STAGE_CHOICES = [
        ('inquiry', 'Inquiry'),
        ('sent_to_lender', 'Sent to Lender'),
        ('funding_table_issued', 'Funding Table Issued'),
        ('iloo_issued', 'ILOO Issued'),
        ('iloo_signed', 'ILOO Signed'),
        ('commitment_fee_paid', 'Commitment Fee Paid'),
        ('app_submitted', 'App Submitted'),
        ('valuation_ordered', 'Valuation Ordered'),
        ('valuation_received', 'Valuation Received'),
        ('more_info_required', 'More Info Required'),
        ('formal_approval', 'Formal Approval'),
        ('loan_docs_instructed', 'Loan Docs Instructed'),
        ('loan_docs_issued', 'Loan Docs Issued'),
        ('loan_docs_signed', 'Loan Docs Signed'),
        ('settlement_conditions', 'Settlement Conditions'),
        ('settled', 'Settled'),
        ('closed', 'Closed'),
        ('declined', 'Declined'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    APPLICATION_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('construction', 'Construction'),
        ('refinance', 'Refinance'),
        ('investment', 'Investment'),
        ('smsf', 'SMSF'),
    ]
    
    REPAYMENT_FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    
    LOAN_PURPOSE_CHOICES = [
        ('purchase', 'Purchase'),
        ('refinance', 'Refinance'),
        ('construction', 'Construction'),
        ('equity_release', 'Equity Release'),
        ('debt_consolidation', 'Debt Consolidation'),
        ('business_expansion', 'Business Expansion'),
        ('working_capital', 'Working Capital'),
        ('other', 'Other'),
    ]
    
    EXIT_STRATEGY_CHOICES = [
        ('sale', 'Sale of Property'),
        ('refinance', 'Refinance'),
        ('income', 'Income/Cash Flow'),
        ('other', 'Other'),
    ]
    
    # Basic application details
    reference_number = models.CharField(max_length=20, unique=True, default=generate_reference_number)
    stage = models.CharField(max_length=25, choices=STAGE_CHOICES, default='inquiry')
    stage_last_updated = models.DateTimeField(default=timezone.now)  # Track when stage was last updated
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True, default='')
    
    # Loan details
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    loan_term = models.PositiveIntegerField(help_text="Loan term in months", null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    repayment_frequency = models.CharField(max_length=20, choices=REPAYMENT_FREQUENCY_CHOICES, default='monthly')
    product_id = models.CharField(max_length=50, null=True, blank=True)
    estimated_settlement_date = models.DateField(null=True, blank=True)
    
    # Loan purpose details
    loan_purpose = models.CharField(max_length=50, choices=LOAN_PURPOSE_CHOICES, null=True, blank=True)
    additional_comments = models.TextField(null=True, blank=True)
    prior_application = models.BooleanField(default=False)
    prior_application_details = models.TextField(null=True, blank=True)
    
    # Exit strategy
    exit_strategy = models.CharField(max_length=50, choices=EXIT_STRATEGY_CHOICES, null=True, blank=True)
    exit_strategy_details = models.TextField(null=True, blank=True)
    
    # General Solvency Enquiries
    has_pending_litigation = models.BooleanField(default=False, help_text="Do the Borrower(s) and the Guarantor(s) have any pending or past litigation matters (within the last 2 years)?")
    has_unsatisfied_judgements = models.BooleanField(default=False, help_text="Are there any unsatisfied judgements against the Borrower(s) and the Guarantor(s)?")
    has_been_bankrupt = models.BooleanField(default=False, help_text="Have the Borrower(s) and the Guarantor(s) been bankrupt or insolvent in the past 5 years?")
    has_been_refused_credit = models.BooleanField(default=False, help_text="Has the Borrower(s) and the Guarantor(s) been refused credit by a credit provider in the last 1 year?")
    has_outstanding_ato_debt = models.BooleanField(default=False, help_text="Are there any outstanding debts current or otherwise due to the ATO by the Borrower(s) and the Guarantor(s)?")
    has_outstanding_tax_returns = models.BooleanField(default=False, help_text="Does the Borrower(s) and the Guarantor(s) have outstanding Tax or BAS returns due to be lodged with the ATO?")
    has_payment_arrangements = models.BooleanField(default=False, help_text="Has the Borrower(s) and the Guarantor(s) made payment arrangements with a creditor to payout debt that is still current?")
    solvency_enquiries_details = models.TextField(null=True, blank=True, help_text="Additional details for any 'Yes' answers to solvency enquiries")
    
    # Funding calculation result
    funding_result = JSONField(null=True, blank=True, help_text="Stores the current funding calculation result")
    
    # Relationships
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='broker_applications')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_applications')
    bd = models.ForeignKey(BDM, on_delete=models.SET_NULL, null=True, related_name='bdm_applications')
    borrowers = models.ManyToManyField('borrowers.Borrower', related_name='borrower_applications')
    guarantors = models.ManyToManyField('borrowers.Guarantor', related_name='guaranteed_applications', blank=True)
    
    # Signature and document info
    signed_by = models.CharField(max_length=255, null=True, blank=True)
    signature_date = models.DateField(null=True, blank=True)
    uploaded_pdf_path = models.FileField(upload_to='applications/signed_forms/', null=True, blank=True)
    
    # Valuer information (flat fields)
    valuer_company_name = models.CharField(max_length=255, null=True, blank=True)
    valuer_contact_name = models.CharField(max_length=255, null=True, blank=True)
    valuer_phone = models.CharField(max_length=20, null=True, blank=True)
    valuer_email = models.EmailField(null=True, blank=True)
    valuation_date = models.DateField(null=True, blank=True)
    valuation_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Quantity Surveyor information (flat fields)
    qs_company_name = models.CharField(max_length=255, null=True, blank=True)
    qs_contact_name = models.CharField(max_length=255, null=True, blank=True)
    qs_phone = models.CharField(max_length=20, null=True, blank=True)
    qs_email = models.EmailField(null=True, blank=True)
    qs_report_date = models.DateField(null=True, blank=True)
    
    # Security property details (legacy fields)
    security_address = models.TextField(null=True, blank=True)
    security_type = models.CharField(max_length=50, null=True, blank=True)
    security_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_applications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_number} - {self.get_stage_display()}"
    
    def save(self, *args, **kwargs):
        # Generate reference number if not provided
        if not self.reference_number:
            self.reference_number = generate_reference_number()
        
        # Check if stage has changed
        if self.pk:
            old_instance = Application.objects.get(pk=self.pk)
            if old_instance.stage != self.stage:
                from django.utils import timezone
                self.stage_last_updated = timezone.now()
        
        super().save(*args, **kwargs)


class SecurityProperty(models.Model):
    """
    Model for security properties
    """
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('retail', 'Retail'),
        ('land', 'Land'),
        ('rural', 'Rural'),
        ('other', 'Other'),
    ]
    
    OCCUPANCY_CHOICES = [
        ('owner_occupied', 'Owner Occupied'),
        ('investment', 'Investment Property'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='security_properties')
    
    # Property address
    address_unit = models.CharField(max_length=20, null=True, blank=True)
    address_street_no = models.CharField(max_length=20, null=True, blank=True)
    address_street_name = models.CharField(max_length=100, null=True, blank=True)
    address_suburb = models.CharField(max_length=100, null=True, blank=True)
    address_state = models.CharField(max_length=50, null=True, blank=True)
    address_postcode = models.CharField(max_length=10, null=True, blank=True)
    
    # Mortgage details
    current_mortgagee = models.CharField(max_length=255, null=True, blank=True)
    first_mortgage = models.CharField(max_length=255, null=True, blank=True)
    second_mortgage = models.CharField(max_length=255, null=True, blank=True)
    current_debt_position = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Property type
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, null=True, blank=True)
    
    # Description
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    car_spaces = models.PositiveIntegerField(null=True, blank=True)
    building_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Size in square meters")
    land_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Size in square meters")
    
    # Structure
    is_single_story = models.BooleanField(default=True)
    has_garage = models.BooleanField(default=False)
    has_carport = models.BooleanField(default=False)
    has_off_street_parking = models.BooleanField(default=False)
    
    # Occupancy
    occupancy = models.CharField(max_length=20, choices=OCCUPANCY_CHOICES, null=True, blank=True)
    
    # Valuation
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        address_parts = [
            self.address_unit,
            self.address_street_no,
            self.address_street_name,
            self.address_suburb,
            self.address_state,
            self.address_postcode
        ]
        address = ' '.join(filter(None, address_parts))
        return f"{address} - {self.estimated_value}"


class LoanRequirement(models.Model):
    """
    Model for loan requirements
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='loan_requirements')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.description} - {self.amount}"


class Document(models.Model):
    """
    Model for application documents
    """
    DOCUMENT_TYPE_CHOICES = [
        ('id', 'Identification'),
        ('income', 'Income Verification'),
        ('bank_statement', 'Bank Statement'),
        ('property', 'Property Document'),
        ('application', 'Application Form'),
        ('contract', 'Contract'),
        ('valuation', 'Valuation Report'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_documents', null=True, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    
    def __str__(self):
        if self.application:
            return f"{self.get_document_type_display()} - {self.application.reference_number}"
        return f"{self.get_document_type_display()} - No Application"


class Fee(models.Model):
    """
    Model for application fees
    """
    FEE_TYPE_CHOICES = [
        ('application', 'Application Fee'),
        ('valuation', 'Valuation Fee'),
        ('legal', 'Legal Fee'),
        ('broker', 'Broker Commission'),
        ('settlement', 'Settlement Fee'),
        ('other', 'Other Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
        ('refunded', 'Refunded'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_fees', null=True, blank=True)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='other')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        fee_type = self.get_fee_type_display() if self.fee_type else "Fee"
        amount = self.amount if self.amount else 0
        return f"{fee_type} - {amount}"


class FundingCalculationHistory(models.Model):
    """
    Model for storing funding calculation history for auditing and compliance
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='funding_calculations')
    calculation_input = JSONField(help_text="Full set of manual input fields used during calculation")
    calculation_result = JSONField(help_text="Computed funding breakdown (all fees, funds available)")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='funding_calculations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Funding calculation histories"

    def __str__(self):
        return f"Funding calculation for {self.application.reference_number} at {self.created_at}"


class Repayment(models.Model):
    """
    Model for loan repayments
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('paid', 'Paid'),
        ('missed', 'Missed'),
        ('partial', 'Partial Payment'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='app_repayments', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    paid_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoice = models.FileField(upload_to='repayment_invoices/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        due_date = self.due_date if self.due_date else "No date"
        amount = self.amount if self.amount else 0
        return f"Repayment {due_date} - {amount}"