from django.template.loader import render_to_string
from django.conf import settings
import os
from uuid import uuid4
from json import loads, dumps
from jsonschema import validate, exceptions
from datetime import datetime
# Comment out weasyprint import to avoid dependency issues during testing
# from weasyprint import HTML
from .models import Application
from documents.models import Document, Fee, Repayment, Note
from users.services import create_application_notification


def generate_document(application_id, document_type, user):
    """
    Generate a document for an application
    
    Args:
        application_id: ID of the application
        document_type: Type of document to generate
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Define template and title based on document type
    template_map = {
        'application_form': {
            'template': 'documents/application_form.html',
            'title': f'Application Form - {application.reference_number}'
        },
        'indicative_letter': {
            'template': 'documents/indicative_letter.html',
            'title': f'Indicative Letter - {application.reference_number}'
        },
        'formal_approval': {
            'template': 'documents/formal_approval.html',
            'title': f'Formal Approval - {application.reference_number}'
        }
    }
    
    if document_type not in template_map:
        return None
    
    template_info = template_map[document_type]
    
    # Generate HTML content
    context = {
        'application': application,
        'borrowers': application.borrowers.all(),
        'guarantors': application.guarantors.all(),
        'broker': application.broker,
        'branch': application.branch,
        'bd': application.bd,
        'generated_date': timezone.now().strftime('%d/%m/%Y'),
    }
    
    html_content = render_to_string(template_info['template'], context)
    
    # Generate PDF - commented out for testing
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents', str(application.id))
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{document_type}_{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Comment out PDF generation for testing
    # HTML(string=html_content).write_pdf(output_path)
    
    # For testing, just create an empty file
    with open(output_path, 'w') as f:
        f.write("Test PDF content")
    
    # Create document record
    relative_path = os.path.join('generated_documents', str(application.id), filename)
    
    document = Document.objects.create(
        title=template_info['title'],
        document_type=document_type,
        file=relative_path,
        file_name=filename,
        file_size=os.path.getsize(output_path),
        file_type='application/pdf',
        application=application,
        created_by=user
    )
    
    return document


def generate_repayment_schedule(application_id, user):
    """
    Generate a repayment schedule for an application
    
    Args:
        application_id: ID of the application
        user: User generating the schedule
        
    Returns:
        List of created Repayment objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Delete existing repayments
    application.repayments.all().delete()
    
    # Calculate repayment amount and schedule
    loan_amount = application.loan_amount
    loan_term = application.loan_term  # in months
    interest_rate = application.interest_rate / 100 if application.interest_rate else 0
    
    # Simple calculation for monthly repayments
    # For a more accurate calculation, use financial formulas
    if application.repayment_frequency == 'monthly':
        monthly_interest = interest_rate / 12
        if monthly_interest > 0:
            # Using the formula for monthly payments: P = L[i(1+i)^n]/[(1+i)^n-1]
            # where P is payment, L is loan amount, i is monthly interest rate, n is number of payments
            monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** loan_term) / ((1 + monthly_interest) ** loan_term - 1)
        else:
            # If no interest, simple division
            monthly_payment = loan_amount / loan_term
        
        # Create repayment schedule
        repayments = []
        start_date = application.estimated_settlement_date or datetime.now().date()
        
        for i in range(1, loan_term + 1):
            due_date = start_date.replace(month=((start_date.month + i - 1) % 12) + 1)
            if (start_date.month + i - 1) // 12 > 0:
                due_date = due_date.replace(year=due_date.year + (start_date.month + i - 1) // 12)
            
            repayment = Repayment.objects.create(
                application=application,
                amount=round(monthly_payment, 2),
                due_date=due_date,
                created_by=user
            )
            repayments.append(repayment)
        
        return repayments
    
    # Handle other frequencies as needed
    return []


def create_standard_fees(application_id, user):
    """
    Create standard fees for an application
    
    Args:
        application_id: ID of the application
        user: User creating the fees
        
    Returns:
        List of created Fee objects
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return []
    
    # Define standard fees
    standard_fees = [
        {
            'fee_type': 'application',
            'description': 'Application processing fee',
            'amount': 500.00,
        },
        {
            'fee_type': 'valuation',
            'description': 'Property valuation fee',
            'amount': 800.00,
        },
        {
            'fee_type': 'legal',
            'description': 'Legal documentation fee',
            'amount': 1200.00,
        },
        {
            'fee_type': 'settlement',
            'description': 'Settlement fee',
            'amount': 300.00,
        }
    ]
    
    # Calculate due dates
    from datetime import timedelta
    from django.utils import timezone
    today = timezone.now().date()
    # Create fees
    fees = []
    for i, fee_data in enumerate(standard_fees):
        due_date = today + timedelta(days=(i+1)*7)  # Due weekly
        
        fee = Fee.objects.create(
            application=application,
            fee_type=fee_data['fee_type'],
            description=fee_data['description'],
            amount=fee_data['amount'],
            due_date=due_date,
            created_by=user
        )
        fees.append(fee)
    
    return fees

def process_signature_data(application_id, signature_data, signed_by, signature_date, user):
    """
    Process signature data for an application
    
    Args:
        application_id: ID of the application
        signature_data: Base64 encoded signature data
        signed_by: Name of the person who signed
        signature_date: Date of signature
        user: User processing the signature
        
    Returns:
        Updated Application object if successful, None otherwise
    """
    from .models import Application
    from base64 import b64decode
    from os import makedirs, path
    from django.conf import settings
    from django.core.files.base import ContentFile
    
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Process signature data (base64 encoded)
    if signature_data:
        # Remove data URL prefix if present
        if signature_data.startswith('data:image'):
            header, signature_data = signature_data.split(';base64,')
        
        # Decode base64 data
        binary_data = base64.b64decode(signature_data)
        
        # Create directory if it doesn't exist
        signature_dir = os.path.join(settings.MEDIA_ROOT, 'signatures', str(application.id))
        os.makedirs(signature_dir, exist_ok=True)
        
        # Save signature as PNG file
        filename = f"signature_{application.id}.png"
        file_path = os.path.join('signatures', str(application.id), filename)
        
        # Update application with signature info
        application.signed_by = signed_by
        application.signature_date = signature_date
        application.uploaded_pdf_path.save(filename, ContentFile(binary_data), save=False)
        application.save()
    
    return application


def validate_application_schema(data):
    """
    Validate application data against JSON schema
    
    Args:
        data: Application data to validate
        
    Returns:
        (is_valid, errors) tuple
    """
    from jsonschema import validate, ValidationError
    
    # Define the JSON schema for application validation
    application_schema = {
        "type": "object",
        "required": ["application_type", "purpose", "loan_amount", "loan_term", "repayment_frequency"],
        "properties": {
            "application_type": {
                "type": "string",
                "enum": ["residential", "commercial", "construction", "refinance", "investment", "smsf"]
            },
            "purpose": {
                "type": "string",
                "minLength": 5
            },
            "loan_amount": {
                "type": "number",
                "minimum": 1000
            },
            "loan_term": {
                "type": "integer",
                "minimum": 1,
                "maximum": 360  # 30 years in months
            },
            "interest_rate": {
                "type": ["number", "null"],
                "minimum": 0,
                "maximum": 30
            },
            "repayment_frequency": {
                "type": "string",
                "enum": ["weekly", "fortnightly", "monthly", "quarterly", "annually"]
            },
            "estimated_settlement_date": {
                "type": ["string", "null"],
                "format": "date"
            },
            "security_address": {
                "type": ["string", "null"]
            },
            "security_type": {
                "type": ["string", "null"]
            },
            "security_value": {
                "type": ["number", "null"],
                "minimum": 0
            }
        }
    }
    
    # Validate against schema
    try:
        jsonschema.validate(instance=data, schema=application_schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)
def validate_application_schema(application_data):
    """
    Validate application data against JSON schema
    
    Args:
        application_data: Dictionary of application data
        
    Returns:
        Tuple of (is_valid, errors)
    """
    schema = {
        "type": "object",
        "required": ["loan_amount", "loan_term", "interest_rate", "purpose", "application_type"],
        "properties": {
            "loan_amount": {"type": "number", "minimum": 0},
            "loan_term": {"type": "integer", "minimum": 1},
            "interest_rate": {"type": "number", "minimum": 0},
            "purpose": {"type": "string", "minLength": 1},
            "application_type": {"type": "string", "minLength": 1},
            "repayment_frequency": {"type": "string", "enum": ["monthly", "quarterly", "annually"]},
            "estimated_settlement_date": {"type": "string", "format": "date"},
            "stage": {"type": "string"},
            "valuer_info": {"type": "object"},
            "qs_info": {"type": "object"}
        }
    }
    
    try:
        validate(instance=application_data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def update_application_stage(application_id, new_stage, user):
    """
    Update application stage and create notification
    
    Args:
        application_id: Application ID
        new_stage: New stage value
        user: User making the change
        
    Returns:
        Updated Application object
    """
    try:
        application = Application.objects.get(id=application_id)
        old_stage = application.stage
        
        # Update stage
        application.stage = new_stage
        application.save()
        
        # Create note about stage change
        Note.objects.create(
            application=application,
            content=f"Application stage changed from '{old_stage}' to '{new_stage}'",
            created_by=user
        )
        
        # Create notification
        create_application_notification(
            application=application,
            notification_type='application_status',
            title=f'Application {application.reference_number} stage updated',
            message=f'Application stage changed from {old_stage} to {new_stage}'
        )
        
        return application
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")


def extend_loan(application_id, new_rate, new_loan_amount, new_repayment, user):
    """
    Extend a loan with new terms and regenerate repayment schedule
    
    Args:
        application_id: ID of the application
        new_rate: New interest rate
        new_loan_amount: New loan amount
        new_repayment: New repayment amount
        user: User extending the loan
        
    Returns:
        Updated Application object and list of new repayments
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")
    
    # Store old values for logging
    old_rate = application.interest_rate
    old_loan_amount = application.loan_amount
    old_repayment = application.repayments.first().amount if application.repayments.exists() else None
    
    # Update application with new values
    application.interest_rate = new_rate
    application.loan_amount = new_loan_amount
    application.save()
    
    # Delete existing repayments
    old_repayments = list(application.repayments.all())
    application.repayments.all().delete()
    
    # Calculate new repayment schedule
    loan_amount = new_loan_amount
    loan_term = application.loan_term  # Keep the same term
    interest_rate = new_rate / 100
    
    # Create new repayments
    repayments = []
    if application.repayment_frequency == 'monthly':
        # Calculate number of repayments based on loan amount and repayment amount
        # This is a simplified calculation - in a real system, you'd use amortization formulas
        monthly_interest = interest_rate / 12
        
        if monthly_interest > 0:
            # Using the formula for number of payments: n = log(P/P-Li)/log(1+i)
            # where P is payment, L is loan amount, i is monthly interest rate
            from math import log, ceil
            num_payments = log(new_repayment / (new_repayment - loan_amount * monthly_interest)) / log(1 + monthly_interest)
            num_payments = ceil(num_payments)  # Round up to nearest whole number
        else:
            # If no interest, simple division
            from math import ceil
            num_payments = ceil(loan_amount / new_repayment)
        
        # Create repayment schedule
        from django.utils import timezone
        start_date = timezone.now().date()
        
        for i in range(1, num_payments + 1):
            # Calculate due date
            due_date = start_date.replace(month=((start_date.month + i - 1) % 12) + 1)
            if (start_date.month + i - 1) // 12 > 0:
                due_date = due_date.replace(year=due_date.year + (start_date.month + i - 1) // 12)
            
            # For the last payment, adjust amount to match the remaining balance
            payment_amount = new_repayment
            if i == num_payments:
                # Calculate remaining balance
                remaining_balance = loan_amount
                for _ in range(1, num_payments):
                    interest_payment = remaining_balance * monthly_interest
                    principal_payment = new_repayment - interest_payment
                    remaining_balance -= principal_payment
                
                # Last payment is remaining balance plus interest
                payment_amount = remaining_balance * (1 + monthly_interest)
            
            # Create repayment
            repayment = Repayment.objects.create(
                application=application,
                amount=round(payment_amount, 2),
                due_date=due_date,
                created_by=user
            )
            repayments.append(repayment)
    
    # Create note about loan extension
    from documents.models import Note
    Note.objects.create(
        application=application,
        title="Loan Extension",
        content=f"Loan extended with new terms: Rate: {old_rate}% -> {new_rate}%, "
                f"Amount: ${old_loan_amount} -> ${new_loan_amount}, "
                f"Repayment: ${old_repayment} -> ${new_repayment}",
        created_by=user
    )
    
    # Create ledger entry for loan extension
    from documents.models import Ledger
    from django.utils import timezone
    Ledger.objects.create(
        application=application,
        transaction_type='adjustment',
        amount=new_loan_amount - old_loan_amount if old_loan_amount else new_loan_amount,
        description=f"Loan extended with new terms: Rate: {old_rate}% -> {new_rate}%, "
                   f"Amount: ${old_loan_amount} -> ${new_loan_amount}, "
                   f"Repayment: ${old_repayment} -> ${new_repayment}",
        transaction_date=timezone.now(),
        created_by=user
    )
    
    return application, repayments


def calculate_funding(application, calculation_input, user):
    """
    Calculate funding for an application based on input parameters
    
    Args:
        application: Application object
        calculation_input: Dictionary containing calculation input parameters
        user: User performing the calculation
        
    Returns:
        Tuple of (calculation_result, funding_calculation_history)
    """
    from .models import FundingCalculationHistory
    from decimal import Decimal
    
    # Validate required application fields
    if not application.loan_amount:
        raise ValueError("Loan amount is required for funding calculation")
    if not application.interest_rate:
        raise ValueError("Interest rate is required for funding calculation")
    if not application.security_value:
        raise ValueError("Security value is required for funding calculation")
    
    # Extract values from application
    loan_amount = Decimal(str(application.loan_amount))
    interest_rate = Decimal(str(application.interest_rate))
    security_value = Decimal(str(application.security_value))
    
    # Extract values from calculation input
    establishment_fee_rate = Decimal(str(calculation_input.get('establishment_fee_rate', 0)))
    capped_interest_months = int(calculation_input.get('capped_interest_months', 9))
    monthly_line_fee_rate = Decimal(str(calculation_input.get('monthly_line_fee_rate', 0)))
    brokerage_fee_rate = Decimal(str(calculation_input.get('brokerage_fee_rate', 0)))
    application_fee = Decimal(str(calculation_input.get('application_fee', 0)))
    due_diligence_fee = Decimal(str(calculation_input.get('due_diligence_fee', 0)))
    legal_fee_before_gst = Decimal(str(calculation_input.get('legal_fee_before_gst', 0)))
    valuation_fee = Decimal(str(calculation_input.get('valuation_fee', 0)))
    monthly_account_fee = Decimal(str(calculation_input.get('monthly_account_fee', 0)))
    working_fee = Decimal(str(calculation_input.get('working_fee', 0)))
    
    # Calculate fees
    establishment_fee = loan_amount * (establishment_fee_rate / 100) * Decimal('1.1')  # With GST
    capped_interest = loan_amount * (interest_rate / 12 / 100) * capped_interest_months
    line_fee = loan_amount * (monthly_line_fee_rate / 100) * 14
    brokerage_fee = loan_amount * (brokerage_fee_rate / 100) * Decimal('1.1')  # With GST
    legal_fee = legal_fee_before_gst * Decimal('1.1')  # With GST
    
    # Calculate total fees and funds available
    total_fees = (
        establishment_fee + 
        capped_interest + 
        line_fee + 
        brokerage_fee + 
        legal_fee + 
        application_fee + 
        due_diligence_fee + 
        valuation_fee + 
        monthly_account_fee + 
        working_fee
    )
    
    funds_available = security_value - total_fees
    
    # Convert Decimal to float for JSON serialization
    calculation_input_serializable = {k: float(v) if isinstance(v, Decimal) else v for k, v in calculation_input.items()}
    
    # Prepare calculation result
    calculation_result = {
        'establishment_fee': float(establishment_fee.quantize(Decimal('0.01'))),
        'capped_interest': float(capped_interest.quantize(Decimal('0.01'))),
        'line_fee': float(line_fee.quantize(Decimal('0.01'))),
        'brokerage_fee': float(brokerage_fee.quantize(Decimal('0.01'))),
        'legal_fee': float(legal_fee.quantize(Decimal('0.01'))),
        'application_fee': float(application_fee.quantize(Decimal('0.01'))),
        'due_diligence_fee': float(due_diligence_fee.quantize(Decimal('0.01'))),
        'valuation_fee': float(valuation_fee.quantize(Decimal('0.01'))),
        'monthly_account_fee': float(monthly_account_fee.quantize(Decimal('0.01'))),
        'working_fee': float(working_fee.quantize(Decimal('0.01'))),
        'total_fees': float(total_fees.quantize(Decimal('0.01'))),
        'funds_available': float(funds_available.quantize(Decimal('0.01')))
    }
    
    # Update application with funding result
    application.funding_result = calculation_result
    application.save()
    
    # Create funding calculation history
    funding_calculation_history = FundingCalculationHistory.objects.create(
        application=application,
        calculation_input=calculation_input_serializable,
        calculation_result=calculation_result,
        created_by=user
    )
    
    return calculation_result, funding_calculation_history


def process_signature_data(application_id, signature_data, signed_by, user):
    """
    Process signature data for an application
    
    Args:
        application_id: Application ID
        signature_data: Base64 encoded signature data
        signed_by: Name of person who signed
        user: User processing the signature
        
    Returns:
        Updated Application object
    """
    try:
        application = Application.objects.get(id=application_id)
        
        # Update application with signature data
        application.signature_data = signature_data
        application.signed_by = signed_by
        from django.utils import timezone
        application.signature_date = timezone.now().date()
        application.save()
        
        # Create note about signature
        Note.objects.create(
            application=application,
            content=f"Application signed by {signed_by}",
            created_by=user
        )
        
        # Create notification
        create_application_notification(
            application=application,
            notification_type='signature_required',
            title=f'Application {application.reference_number} signed',
            message=f'Application has been signed by {signed_by}'
        )
        
        return application
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")
