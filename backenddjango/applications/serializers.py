from rest_framework import serializers
from .models import Application, Document, Fee, Repayment, FundingCalculationHistory, SecurityProperty, LoanRequirement
from borrowers.models import Borrower, Guarantor, Director, Asset, Liability
from .validators import validate_company_borrower
from django.db import transaction
from users.serializers import UserSerializer
from brokers.serializers import BrokerDetailSerializer as BrokerSerializer, BDMSerializer, BranchSerializer
from documents.serializers import DocumentSerializer, NoteSerializer, FeeSerializer, RepaymentSerializer, LedgerSerializer
from decimal import Decimal

class SolvencyEnquiriesSerializer(serializers.Serializer):
    """
    Serializer for solvency enquiries summary
    """
    has_solvency_issues = serializers.BooleanField(read_only=True)
    solvency_issues_count = serializers.IntegerField(read_only=True)
    solvency_issues_summary = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        # Count how many solvency issues are marked as True
        solvency_fields = [
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements'
        ]
        
        issues_count = sum(1 for field in solvency_fields if getattr(instance, field, False))
        has_issues = issues_count > 0
        
        # Create a summary of the issues
        issues_summary = []
        if instance.has_pending_litigation:
            issues_summary.append("Has pending/past litigation")
        if instance.has_unsatisfied_judgements:
            issues_summary.append("Has unsatisfied judgements")
        if instance.has_been_bankrupt:
            issues_summary.append("Has bankruptcy history")
        if instance.has_been_refused_credit:
            issues_summary.append("Has been refused credit")
        if instance.has_outstanding_ato_debt:
            issues_summary.append("Has outstanding ATO debt")
        if instance.has_outstanding_tax_returns:
            issues_summary.append("Has outstanding tax returns")
        if instance.has_payment_arrangements:
            issues_summary.append("Has payment arrangements")
        
        summary = ", ".join(issues_summary) if issues_summary else "No solvency issues"
        
        return {
            'has_solvency_issues': has_issues,
            'solvency_issues_count': issues_count,
            'solvency_issues_summary': summary
        }

class GeneratePDFSerializer(serializers.Serializer):
    """
    Serializer for PDF generation endpoint
    """
    template_name = serializers.CharField(required=False)
    output_format = serializers.ChoiceField(choices=['pdf', 'docx'], default='pdf', required=False)

class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)

class EmploymentInfoSerializer(serializers.Serializer):
    employer = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=100)
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    years_employed = serializers.DecimalField(max_digits=5, decimal_places=2)

class BorrowerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    employment_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'address', 'employment_info', 'tax_id', 'marital_status',
            'residency_status', 'referral_source', 'tags'
        ]
    
    def get_address(self, obj) -> dict:
        return {
            'street': obj.residential_address or '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': ''
        }
    
    def get_employment_info(self, obj) -> dict:
        return {
            'employer': obj.employer_name or '',
            'position': obj.job_title or '',
            'income': obj.annual_income or 0,
            'years_employed': obj.employment_duration or 0
        }
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        employment_data = validated_data.pop('employment_info', None)
        
        borrower = Borrower.objects.create(**validated_data)
        
        # Create address and employment info if provided
        if address_data:
            borrower.residential_address = address_data.get('street', '')
        
        if employment_data:
            borrower.employer_name = employment_data.get('employer', '')
            borrower.job_title = employment_data.get('position', '')
            borrower.annual_income = employment_data.get('income', 0)
            borrower.employment_duration = employment_data.get('years_employed', 0)
        
        borrower.save()
        
        return borrower

from .serializers_asset import GuarantorAssetSerializer, CompanyAssetSerializer
from drf_spectacular.utils import extend_schema_field

class ApplicationLiabilitySerializer(serializers.ModelSerializer):
    """Liability serializer specifically for application context"""
    class Meta:
        model = Liability
        fields = ['id', 'liability_type', 'description', 'amount', 'monthly_payment', 'bg_type']

class GuarantorSerializer(serializers.ModelSerializer):
    from .serializers_asset import GuarantorAssetSerializer
    assets = GuarantorAssetSerializer(many=True, required=False, read_only=True)
    liabilities = ApplicationLiabilitySerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Guarantor
        fields = [
            'id', 'guarantor_type', 'title', 'first_name', 'last_name', 'date_of_birth',
            'drivers_licence_no', 'home_phone', 'mobile', 'email',
            'address_unit', 'address_street_no', 'address_street_name',
            'address_suburb', 'address_state', 'address_postcode',
            'occupation', 'employer_name', 'employment_type', 'annual_income',
            'company_name', 'company_abn', 'company_acn',
            'borrower', 'application', 'assets', 'liabilities'
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Ensure assets and liabilities are always lists
        data['assets'] = data.get('assets', [])
        data['liabilities'] = data.get('liabilities', [])
        return data
    
    def create(self, validated_data):
        assets_data = validated_data.pop('assets', [])
        liabilities_data = validated_data.pop('liabilities', [])
        
        # Create the guarantor
        guarantor = Guarantor.objects.create(**validated_data)
        
        # Create assets
        for asset_data in assets_data:
            Asset.objects.create(guarantor=guarantor, **asset_data)
        
        # Create liabilities
        for liability_data in liabilities_data:
            Liability.objects.create(guarantor=guarantor, **liability_data)
        
        return guarantor

class FinancialInfoSerializer(serializers.Serializer):
    annual_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    assets = serializers.DecimalField(max_digits=12, decimal_places=2)
    liabilities = serializers.DecimalField(max_digits=12, decimal_places=2)

class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializer for company directors
    """
    class Meta:
        model = Director
        fields = ['id', 'name', 'roles', 'director_id']


class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for assets
    """
    class Meta:
        model = Asset
        fields = ['id', 'asset_type', 'description', 'value', 'amount_owing', 'to_be_refinanced', 'address', 'bg_type']


class LiabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for liabilities
    """
    class Meta:
        model = Liability
        fields = ['id', 'liability_type', 'description', 'amount', 'lender', 'monthly_payment', 'to_be_refinanced', 'bg_type']


class SecurityPropertySerializer(serializers.ModelSerializer):
    """
    Serializer for security properties
    """
    class Meta:
        model = SecurityProperty
        fields = [
            'id', 'address_unit', 'address_street_no', 'address_street_name', 'address_suburb', 
            'address_state', 'address_postcode', 'current_mortgagee', 'first_mortgage', 
            'second_mortgage', 'current_debt_position', 'property_type', 'bedrooms', 
            'bathrooms', 'car_spaces', 'building_size', 'land_size', 'is_single_story', 
            'has_garage', 'has_carport', 'has_off_street_parking', 'occupancy', 
            'estimated_value', 'purchase_price'
        ]


class LoanRequirementSerializer(serializers.ModelSerializer):
    """
    Serializer for loan requirements
    """
    class Meta:
        model = LoanRequirement
        fields = ['id', 'description', 'amount']

class CompanyBorrowerSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, required=False)
    financial_info = FinancialInfoSerializer(required=False)
    from .serializers_asset import CompanyAssetSerializer
    assets = CompanyAssetSerializer(many=True, required=False)
    liabilities = LiabilitySerializer(many=True, required=False)
    
    class Meta:
        model = Borrower
        fields = [
            'id', 'company_name', 'company_abn', 'company_acn', 'industry_type',
            'contact_number', 'annual_company_income', 'is_trustee', 'is_smsf_trustee',
            'trustee_name', 'registered_address_unit', 'registered_address_street_no',
            'registered_address_street_name', 'registered_address_suburb',
            'registered_address_state', 'registered_address_postcode',
            'directors', 'financial_info', 'assets', 'liabilities'
        ]
        
    def validate(self, data):
        # Use the custom validator for company borrower
        errors = validate_company_borrower(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        directors_data = validated_data.pop('directors', [])
        financial_info = validated_data.pop('financial_info', None)
        assets_data = validated_data.pop('assets', [])
        liabilities_data = validated_data.pop('liabilities', [])
        
        # Create the company borrower
        company = Borrower.objects.create(is_company=True, **validated_data)
        
        # Create directors
        for director_data in directors_data:
            Director.objects.create(borrower=company, **director_data)
        
        # Store financial info as JSON
        if financial_info:
            company.financial_info = financial_info
            company.save()
        
        # Create assets
        for asset_data in assets_data:
            Asset.objects.create(borrower=company, **asset_data)
        
        # Create liabilities
        for liability_data in liabilities_data:
            Liability.objects.create(borrower=company, **liability_data)
        
        return company

# Removed PropertySerializer as it's causing issues with the Application model
# The Application model doesn't have a property field that matches this serializer

class ApplicationSignatureSerializer(serializers.Serializer):
    """
    Serializer for application signature
    """
    signature = serializers.CharField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    signature_date = serializers.DateField(required=False)
    notes = serializers.CharField(allow_blank=True, required=False)

class QSInfoSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    contact_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    notes = serializers.CharField(allow_blank=True, required=False)

class FundingCalculationInputSerializer(serializers.Serializer):
    """
    Serializer for funding calculation input fields
    """
    establishment_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    capped_interest_months = serializers.IntegerField(min_value=1, default=9)
    monthly_line_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    brokerage_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    legal_fee_before_gst = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)


class ManualFundingCalculationSerializer(serializers.Serializer):
    """
    Serializer for manual funding calculation with application parameters
    """
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    security_value = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    
    # Include all funding calculation input fields
    establishment_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    capped_interest_months = serializers.IntegerField(min_value=1, default=9)
    monthly_line_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    brokerage_fee_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    legal_fee_before_gst = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)


class ApplicationCreateSerializer(serializers.ModelSerializer):
    borrowers = BorrowerSerializer(many=True, required=False)
    guarantors = GuarantorSerializer(many=True, required=False)
    company_borrowers = CompanyBorrowerSerializer(many=True, required=False)
    security_properties = SecurityPropertySerializer(many=True, required=False)
    loan_requirements = LoanRequirementSerializer(many=True, required=False)
    
    # Add funding calculation input fields
    funding_calculation_input = FundingCalculationInputSerializer(required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'product_id', 'estimated_settlement_date',
            'stage', 'branch_id', 'bd_id', 'borrowers', 'guarantors',
            'company_borrowers', 'security_properties', 'loan_requirements',
            'loan_purpose', 'additional_comments', 'prior_application',
            'prior_application_details', 'exit_strategy', 'exit_strategy_details',
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'qs_company_name', 'qs_contact_name', 'qs_phone', 'qs_email',
            'funding_calculation_input',
            # General Solvency Enquiries
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements', 'solvency_enquiries_details'
        ]
    
    def create(self, validated_data):
        borrowers_data = validated_data.pop('borrowers', [])
        guarantors_data = validated_data.pop('guarantors', [])
        company_borrowers_data = validated_data.pop('company_borrowers', [])
        security_properties_data = validated_data.pop('security_properties', [])
        loan_requirements_data = validated_data.pop('loan_requirements', [])
        funding_calculation_input = validated_data.pop('funding_calculation_input', None)
        
        # Process new_borrowers data if present in the request
        new_borrowers = validated_data.pop('new_borrowers', [])
        
        # Use transaction to ensure all related entities are created or none
        with transaction.atomic():
            # Create the application
            application = Application.objects.create(**validated_data)
            
            # Create borrowers and link to application
            for borrower_data in borrowers_data:
                borrower_serializer = BorrowerSerializer(data=borrower_data)
                borrower_serializer.is_valid(raise_exception=True)
                borrower = borrower_serializer.save()
                application.borrowers.add(borrower)
            
            # Process new_borrowers if present
            for new_borrower_data in new_borrowers:
                # Create a new borrower
                borrower = Borrower.objects.create(
                    first_name=new_borrower_data.get('first_name', ''),
                    last_name=new_borrower_data.get('last_name', ''),
                    date_of_birth=new_borrower_data.get('date_of_birth'),
                    email=new_borrower_data.get('email', ''),
                    phone=new_borrower_data.get('phone', ''),
                    residential_address=new_borrower_data.get('residential_address', ''),
                    marital_status=new_borrower_data.get('marital_status', ''),
                    residency_status=new_borrower_data.get('residency_status', ''),
                    employment_type=new_borrower_data.get('employment_type', ''),
                    employer_name=new_borrower_data.get('employer_name', ''),
                    annual_income=new_borrower_data.get('annual_income', 0),
                    created_by=validated_data.get('created_by')
                )
                # Add the borrower to the application
                application.borrowers.add(borrower)
            
            # Create guarantors and link to application
            for guarantor_data in guarantors_data:
                guarantor_serializer = GuarantorSerializer(data=guarantor_data)
                guarantor_serializer.is_valid(raise_exception=True)
                guarantor = guarantor_serializer.save(application=application)
                application.guarantors.add(guarantor)
            
            # Process guarantor_data if present
            guarantor_data_list = validated_data.pop('guarantor_data', [])
            for guarantor_data in guarantor_data_list:
                # Create a new guarantor
                guarantor = Guarantor.objects.create(
                    guarantor_type=guarantor_data.get('guarantor_type', ''),
                    title=guarantor_data.get('title', ''),
                    first_name=guarantor_data.get('first_name', ''),
                    last_name=guarantor_data.get('last_name', ''),
                    date_of_birth=guarantor_data.get('date_of_birth'),
                    drivers_licence_no=guarantor_data.get('drivers_licence_no', ''),
                    home_phone=guarantor_data.get('home_phone', ''),
                    mobile=guarantor_data.get('mobile', ''),
                    email=guarantor_data.get('email', ''),
                    address_unit=guarantor_data.get('address_unit', ''),
                    address_street_no=guarantor_data.get('address_street_no', ''),
                    address_street_name=guarantor_data.get('address_street_name', ''),
                    address_suburb=guarantor_data.get('address_suburb', ''),
                    address_state=guarantor_data.get('address_state', ''),
                    address_postcode=guarantor_data.get('address_postcode', ''),
                    occupation=guarantor_data.get('occupation', ''),
                    employer_name=guarantor_data.get('employer_name', ''),
                    employment_type=guarantor_data.get('employment_type', ''),
                    annual_income=guarantor_data.get('annual_income', 0),
                    application=application,
                    created_by=validated_data.get('created_by')
                )
                # If borrower_id is provided, link the guarantor to the borrower
                borrower_id = guarantor_data.get('borrower_id')
                if borrower_id:
                    try:
                        borrower = Borrower.objects.get(id=borrower_id)
                        guarantor.borrower = borrower
                        guarantor.save()
                    except Borrower.DoesNotExist:
                        pass
            
            # Create company borrowers and link to application
            for company_data in company_borrowers_data:
                company_serializer = CompanyBorrowerSerializer(data=company_data)
                company_serializer.is_valid(raise_exception=True)
                company = company_serializer.save()
                application.borrowers.add(company)  # Add to borrowers since it's a Borrower model with is_company=True
            
            # Create security properties
            for security_property_data in security_properties_data:
                SecurityProperty.objects.create(
                    application=application,
                    **security_property_data
                )
            
            # Create loan requirements
            for loan_requirement_data in loan_requirements_data:
                LoanRequirement.objects.create(
                    application=application,
                    **loan_requirement_data
                )
            
            application.save()
            
            # Perform funding calculation if input is provided
            if funding_calculation_input and application.loan_amount and application.interest_rate and application.security_value:
                from .services import calculate_funding
                try:
                    calculation_result, funding_history = calculate_funding(
                        application=application,
                        calculation_input=funding_calculation_input,
                        user=validated_data.get('created_by')
                    )
                    
                    # Create note about funding calculation
                    from documents.models import Note
                    Note.objects.create(
                        application=application,
                        content=f"Initial funding calculation performed: Total fees ${calculation_result['total_fees']}, Funds available ${calculation_result['funds_available']}",
                        created_by=validated_data.get('created_by')
                    )
                except Exception as e:
                    # Log the error but don't fail the application creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error performing initial funding calculation: {str(e)}")
            
            # Create notification for new application
            from users.models import Notification
            if application.bd_id:
                Notification.objects.create(
                    user_id=application.bd_id,  # Notify the BD
                    title=f"New Application: {application.reference_number}",
                    message=f"A new loan application has been submitted with reference {application.reference_number}",
                    notification_type="application_created",
                    related_object_id=application.id
                )
            
            return application



class ApplicationDetailSerializer(serializers.ModelSerializer):
    # Basic application fields are included by default
    
    # Related entities
    borrowers = BorrowerSerializer(many=True, read_only=True)
    guarantors = GuarantorSerializer(many=True, read_only=True)
    security_properties = SecurityPropertySerializer(many=True, read_only=True)
    loan_requirements = LoanRequirementSerializer(many=True, read_only=True)
    
    # Documents and notes
    documents = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    
    # Financial tracking
    fees = serializers.SerializerMethodField()
    repayments = serializers.SerializerMethodField()
    ledger_entries = serializers.SerializerMethodField()
    
    # Related parties
    broker = BrokerSerializer(read_only=True)
    bd = BDMSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    
    # Status information
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            # Basic fields
            'id', 'reference_number', 'loan_amount', 'loan_term',
            'interest_rate', 'purpose', 'repayment_frequency',
            'application_type', 'product_id', 'estimated_settlement_date',
            'stage', 'stage_display', 'created_at', 'updated_at',
            
            # Loan purpose details
            'loan_purpose', 'additional_comments', 'prior_application',
            'prior_application_details',
            
            # Exit strategy
            'exit_strategy', 'exit_strategy_details',
            
            # General Solvency Enquiries
            'has_pending_litigation', 'has_unsatisfied_judgements', 'has_been_bankrupt',
            'has_been_refused_credit', 'has_outstanding_ato_debt', 'has_outstanding_tax_returns',
            'has_payment_arrangements', 'solvency_enquiries_details',
            
            # Related entities
            'borrowers', 'guarantors', 'broker', 'bd', 'branch',
            'security_properties', 'loan_requirements',
            
            # Documents and notes
            'documents', 'notes',
            
            # Financial tracking
            'fees', 'repayments', 'ledger_entries',
            
            # Security property details (legacy fields)
            'security_address', 'security_type', 'security_value',
            
            # Valuer information
            'valuer_company_name', 'valuer_contact_name', 'valuer_phone',
            'valuer_email', 'valuation_date', 'valuation_amount',
            
            # QS information
            'qs_company_name', 'qs_contact_name', 'qs_phone',
            'qs_email', 'qs_report_date',
            
            # Signature and PDF
            'signed_by', 'signature_date', 'uploaded_pdf_path',
            
            # Funding calculation
            'funding_result',
            
            # Metadata
            'created_by_details'
        ]
    
    def get_documents(self, obj) -> list:
        documents = Document.objects.filter(application=obj)
        return DocumentSerializer(documents, many=True, context=self.context).data
    
    def get_notes(self, obj) -> list:
        from documents.models import Note
        notes = Note.objects.filter(application=obj).order_by('-created_at')
        return NoteSerializer(notes, many=True, context=self.context).data
    
    def get_fees(self, obj) -> list:
        fees = Fee.objects.filter(application=obj)
        return FeeSerializer(fees, many=True, context=self.context).data
    
    def get_repayments(self, obj) -> list:
        repayments = Repayment.objects.filter(application=obj).order_by('due_date')
        return RepaymentSerializer(repayments, many=True, context=self.context).data
    
    def get_ledger_entries(self, obj) -> list:
        from documents.models import Ledger
        ledger_entries = Ledger.objects.filter(application=obj).order_by('-transaction_date')
        return LedgerSerializer(ledger_entries, many=True, context=self.context).data
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Ensure all expected fields are present with defaults
        data['borrowers'] = data.get('borrowers', [])
        data['guarantors'] = data.get('guarantors', [])
        data['security_properties'] = data.get('security_properties', [])
        data['loan_requirements'] = data.get('loan_requirements', [])
        data['documents'] = data.get('documents', [])
        data['notes'] = data.get('notes', [])
        data['fees'] = data.get('fees', [])
        data['repayments'] = data.get('repayments', [])
        data['ledger_entries'] = data.get('ledger_entries', [])
        
        # Ensure each guarantor has assets and liabilities
        for guarantor in data['guarantors']:
            guarantor['assets'] = guarantor.get('assets', [])
            guarantor['liabilities'] = guarantor.get('liabilities', [])
            
        return data

class ApplicationStageUpdateSerializer(serializers.Serializer):
    stage = serializers.ChoiceField(choices=Application.STAGE_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)

class ApplicationBorrowerSerializer(serializers.Serializer):
    borrower_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )

class ApplicationListSerializer(serializers.ModelSerializer):
    """Serializer for listing applications with summary information"""
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    borrower_count = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()
    guarantor_name = serializers.SerializerMethodField()
    bdm_name = serializers.SerializerMethodField()
    security_address = serializers.SerializerMethodField()
    purpose = serializers.CharField(source='loan_purpose', read_only=True)
    product_name = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(read_only=True)
    solvency_issues = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id', 'reference_number', 'borrower_name', 'stage', 'stage_display',
            'bdm_name', 'guarantor_name', 'purpose', 'product_name', 'security_address',
            'loan_amount', 'estimated_settlement_date', 'updated_at', 'created_at',
            'application_type', 'borrower_count', 'solvency_issues'
        ]
    
    def get_borrower_count(self, obj) -> int:
        return obj.borrowers.count()
    
    def get_borrower_name(self, obj) -> str:
        """Get the primary borrower name(s)"""
        borrowers = obj.borrowers.all()
        if not borrowers:
            return ""
        
        names = []
        for borrower in borrowers:
            if borrower.is_company:
                if borrower.company_name:
                    names.append(borrower.company_name)
            else:
                name = f"{borrower.first_name} {borrower.last_name}".strip()
                if name:
                    names.append(name)
        
        return ", ".join(names) if names else ""
    
    def get_guarantor_name(self, obj) -> str:
        """Get the guarantor name(s)"""
        guarantors = obj.guarantors.all()
        if not guarantors:
            return ""
        
        names = []
        for guarantor in guarantors:
            name = f"{guarantor.first_name} {guarantor.last_name}".strip()
            if name:
                names.append(name)
        
        return ", ".join(names) if names else ""
    
    def get_bdm_name(self, obj) -> str:
        """Get the BDM name"""
        if hasattr(obj, 'bd') and obj.bd:
            return obj.bd.name
        return ""
    
    def get_security_address(self, obj) -> str:
        """Get the security property address"""
        # First try to get from security_properties
        from applications.models import SecurityProperty
        security_properties = SecurityProperty.objects.filter(application=obj)
        if security_properties:
            prop = security_properties[0]
            address_parts = [
                prop.address_unit,
                prop.address_street_no,
                prop.address_street_name,
                prop.address_suburb,
                prop.address_state,
                prop.address_postcode
            ]
            address = " ".join(part for part in address_parts if part)
            return address
        
        # Fall back to legacy field
        return obj.security_address or ""
    
    def get_product_name(self, obj) -> str:
        """Get the product name"""
        if obj.product_id:
            try:
                from products.models import Product
                product = Product.objects.get(id=obj.product_id)
                return product.name
            except:
                return f"Product {obj.product_id}"
        return ""
        
    def get_solvency_issues(self, obj) -> dict:
        """Get solvency issues summary"""
        serializer = SolvencyEnquiriesSerializer(obj)
        return serializer.data


class FundingCalculationHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for funding calculation history
    """
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = FundingCalculationHistory
        fields = [
            'id', 'application', 'calculation_input', 'calculation_result', 
            'created_by', 'created_by_details', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']


class FundingCalculationResultSerializer(serializers.Serializer):
    """
    Serializer for funding calculation result
    """
    establishment_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    capped_interest = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    line_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    brokerage_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    legal_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    application_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    due_diligence_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    monthly_account_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    working_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_fees = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    funds_available = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class LoanExtensionSerializer(serializers.Serializer):
    """
    Serializer for extending a loan with new terms
    """
    new_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    new_loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    new_repayment = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    def validate(self, data):
        """
        Validate the loan extension data
        """
        # Ensure new_rate is positive
        if data['new_rate'] <= Decimal('0'):
            raise serializers.ValidationError({"new_rate": "Interest rate must be greater than 0"})
        
        # Ensure new_loan_amount is positive
        if data['new_loan_amount'] <= Decimal('0'):
            raise serializers.ValidationError({"new_loan_amount": "Loan amount must be greater than 0"})
        
        # Ensure new_repayment is positive
        if data['new_repayment'] <= Decimal('0'):
            raise serializers.ValidationError({"new_repayment": "Repayment amount must be greater than 0"})
        
        # Ensure new_repayment is less than new_loan_amount
        if data['new_repayment'] >= data['new_loan_amount']:
            raise serializers.ValidationError({"new_repayment": "Repayment amount must be less than loan amount"})
        
        return data
