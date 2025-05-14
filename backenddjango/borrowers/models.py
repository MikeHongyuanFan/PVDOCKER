from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Borrower(models.Model):
    """
    Model for borrowers
    """
    RESIDENCY_STATUS_CHOICES = [
        ('citizen', 'Citizen'),
        ('permanent_resident', 'Permanent Resident'),
        ('temporary_resident', 'Temporary Resident'),
        ('foreign_investor', 'Foreign Investor'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('de_facto', 'De Facto'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('casual', 'Casual'),
        ('self_employed', 'Self Employed'),
        ('contractor', 'Contractor'),
        ('unemployed', 'Unemployed'),
        ('retired', 'Retired'),
    ]
    
    INDUSTRY_TYPE_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('mining', 'Mining'),
        ('manufacturing', 'Manufacturing'),
        ('construction', 'Construction'),
        ('retail', 'Retail'),
        ('transport', 'Transport'),
        ('hospitality', 'Hospitality'),
        ('finance', 'Finance'),
        ('real_estate', 'Real Estate'),
        ('professional', 'Professional Services'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('arts', 'Arts and Recreation'),
        ('other', 'Other'),
    ]
    
    # Personal information
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Address information
    residential_address = models.TextField(null=True, blank=True)
    mailing_address = models.TextField(null=True, blank=True)
    
    # Identity information
    tax_id = models.CharField(max_length=50, null=True, blank=True, help_text="Tax File Number or equivalent")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    residency_status = models.CharField(max_length=20, choices=RESIDENCY_STATUS_CHOICES, null=True, blank=True)
    
    # Employment information
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, null=True, blank=True, default='full_time')
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    employer_address = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    employment_duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in months")
    
    # Financial information
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    other_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Bank account information
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_bsb = models.CharField(max_length=10, null=True, blank=True)
    
    # Additional information
    referral_source = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    notes_text = models.TextField(null=True, blank=True)
    
    # Company information (for company borrowers)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_abn = models.CharField(max_length=20, null=True, blank=True)
    company_acn = models.CharField(max_length=20, null=True, blank=True)
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_TYPE_CHOICES, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    annual_company_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_trustee = models.BooleanField(default=False)
    is_smsf_trustee = models.BooleanField(default=False)
    trustee_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Registered address (for company borrowers)
    registered_address_unit = models.CharField(max_length=20, null=True, blank=True)
    registered_address_street_no = models.CharField(max_length=20, null=True, blank=True)
    registered_address_street_name = models.CharField(max_length=100, null=True, blank=True)
    registered_address_suburb = models.CharField(max_length=100, null=True, blank=True)
    registered_address_state = models.CharField(max_length=50, null=True, blank=True)
    registered_address_postcode = models.CharField(max_length=10, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)  # Legacy field
    
    # Relationships
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrower_profile')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_borrowers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.is_company:
            return f"{self.company_name}"
        return f"{self.first_name} {self.last_name}"


class Director(models.Model):
    """
    Model for company directors
    """
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('secretary', 'Secretary'),
        ('public_officer', 'Public Officer'),
        ('shareholder', 'Shareholder'),
    ]
    
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='directors')
    name = models.CharField(max_length=255)
    roles = models.CharField(max_length=255, help_text="Comma-separated list of roles")
    director_id = models.CharField(max_length=50, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.roles}"


class Asset(models.Model):
    """
    Model for borrower and guarantor assets
    """
    ASSET_TYPE_CHOICES = [
        ('Property', 'Property'),
        ('Vehicle', 'Vehicle'),
        ('Savings', 'Savings'),
        ('Investment Shares', 'Investment Shares'),
        ('Credit Card', 'Credit Card'),
        ('Other Creditor', 'Other Creditor'),
        ('Other', 'Other'),
        ('To be refinanced', 'To be refinanced'),  # Only for company assets
    ]
    
    # Use a different name for the choices to avoid collision
    BG_TYPE_CHOICES = [
        ('BG1', 'BG1'),
        ('BG2', 'BG2'),
    ]
    
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='assets', null=True, blank=True)
    guarantor = models.ForeignKey('Guarantor', on_delete=models.CASCADE, related_name='assets', null=True, blank=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True, default='')
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0.00)
    amount_owing = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    to_be_refinanced = models.BooleanField(default=False)  # Only used for company assets
    address = models.TextField(null=True, blank=True)
    bg_type = models.CharField(max_length=10, choices=BG_TYPE_CHOICES, null=True, blank=True, 
                              help_text="Indicates if this asset belongs to BG1 or BG2 (only for guarantor assets)")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_asset_type_display()} - {self.value}"
    
    def clean(self):
        """
        Validate that bg_type is only set for guarantor assets and
        to_be_refinanced is only set for company assets
        """
        from django.core.exceptions import ValidationError
        
        if self.guarantor and not self.bg_type:
            raise ValidationError({"bg_type": "bg_type is required for guarantor assets"})
        
        if not self.guarantor and self.bg_type:
            raise ValidationError({"bg_type": "bg_type should not be set for company assets"})
        
        if self.guarantor and self.to_be_refinanced:
            raise ValidationError({"to_be_refinanced": "to_be_refinanced should not be set for guarantor assets"})


class Liability(models.Model):
    """
    Model for borrower liabilities
    """
    LIABILITY_TYPE_CHOICES = [
        ('mortgage', 'Mortgage'),
        ('personal_loan', 'Personal Loan'),
        ('car_loan', 'Car Loan'),
        ('credit_card', 'Credit Card'),
        ('tax_debt', 'Tax Debt'),
        ('other_creditor', 'Other Creditor'),
        ('other', 'Other'),
    ]
    
    BORROWER_GUARANTOR_CHOICES = [
        ('bg1', 'B/G1'),
        ('bg2', 'B/G2'),
    ]
    
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='liabilities', null=True, blank=True)
    guarantor = models.ForeignKey('Guarantor', on_delete=models.CASCADE, related_name='liabilities', null=True, blank=True)
    liability_type = models.CharField(max_length=20, choices=LIABILITY_TYPE_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    lender = models.CharField(max_length=100, null=True, blank=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    to_be_refinanced = models.BooleanField(default=False)
    bg_type = models.CharField(max_length=10, choices=BORROWER_GUARANTOR_CHOICES, default='bg1', help_text="Indicates if this liability belongs to B/G1 or B/G2")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_liability_type_display()} - {self.amount}"


class Guarantor(models.Model):
    """
    Model for guarantors
    """
    GUARANTOR_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
    ]
    
    TITLE_CHOICES = [
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),
        ('miss', 'Miss'),
        ('dr', 'Dr'),
        ('other', 'Other'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('casual', 'Casual/Temp'),
        ('contract', 'Contract'),
    ]
    
    # Basic information
    guarantor_type = models.CharField(max_length=20, choices=GUARANTOR_TYPE_CHOICES, default='individual')
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    drivers_licence_no = models.CharField(max_length=50, null=True, blank=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    # Address information
    address_unit = models.CharField(max_length=20, null=True, blank=True)
    address_street_no = models.CharField(max_length=20, null=True, blank=True)
    address_street_name = models.CharField(max_length=100, null=True, blank=True)
    address_suburb = models.CharField(max_length=100, null=True, blank=True)
    address_state = models.CharField(max_length=50, null=True, blank=True)
    address_postcode = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Legacy field
    
    # Employment information
    occupation = models.CharField(max_length=100, null=True, blank=True)
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Company information (for company guarantors)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_abn = models.CharField(max_length=20, null=True, blank=True)
    company_acn = models.CharField(max_length=20, null=True, blank=True)
    
    # Relationships
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='borrower_guarantors', null=True, blank=True)
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='application_guarantors', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['guarantor_type', 'last_name', 'first_name', 'company_name']
    
    def __str__(self):
        if self.guarantor_type == 'company':
            return f"{self.company_name} (Company Guarantor)"
        return f"{self.first_name} {self.last_name} (Individual Guarantor)"
