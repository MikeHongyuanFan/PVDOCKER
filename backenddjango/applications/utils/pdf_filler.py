import os
import logging
from typing import List, Dict, Any, Optional
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from django.conf import settings
from ..models import Application

logger = logging.getLogger(__name__)

# Define the mapping between model fields and PDF form fields
FIELD_MAP = {
    # Application fields
    "reference_number": "Text1",
    "loan_amount": "Text2",
    "loan_term": "Text3",
    "interest_rate": "Text4",
    "loan_purpose": "Text5",
    "exit_strategy": "Text6",
    "additional_comments": "Text7",
    "repayment_frequency": "Text8",
    
    # Borrower fields (individual)
    "borrower_first_name": "Text9",
    "borrower_last_name": "Text10",
    "borrower_email": "Text11",
    "borrower_phone": "Text12",
    "borrower_residential_address": "Text13",
    "borrower_annual_income": "Text14",
    
    # Borrower fields (company)
    "company_name": "Text15",
    "company_abn": "Text16",
    "company_acn": "Text17",
    "company_address": "Text18",
    "annual_company_income": "Text19",
    
    # Security property fields
    "security_address": "Text20",
    "security_type": "Text21",
    "security_value": "Text22",
    
    # Loan requirement fields
    "loan_requirement_description": "Text23",
    "loan_requirement_amount": "Text24",
}

def fill_pdf_form(application: Application, output_path: str) -> List[str]:
    """
    Fill a PDF form with data from an Application instance.
    
    Args:
        application: The Application instance to get data from
        output_path: The path where the filled PDF should be saved
        
    Returns:
        A list of field names that were missing from the application
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Get the path to the template PDF
    template_path = os.path.join(
        settings.BASE_DIR, 
        'applications', 
        'ApplicationTemplate', 
        'Eternity Capital - Application Form (1).pdf'
    )
    
    # Check if template exists
    if not os.path.exists(template_path):
        logger.error(f"PDF template not found at {template_path}")
        raise FileNotFoundError(f"PDF template not found at {template_path}")
    
    # Read the template PDF
    template = PdfReader(template_path)
    
    # Prepare data dictionary from application
    data = extract_application_data(application)
    
    # Track missing fields
    missing_fields = []
    
    # Debug: Print all data being used to fill the form
    logger.info(f"Filling PDF form with data: {data}")
    
    # Fill the form fields
    for page in template.pages:
        if page.Annots:
            for annotation in page.Annots:
                if annotation.FT and annotation.FT == '/Tx':  # Text field
                    field_name = annotation.T.strip('()')  # Remove parentheses from field name
                    
                    # Find the corresponding model field
                    model_field = next(
                        (k for k, v in FIELD_MAP.items() if v == field_name), 
                        None
                    )
                    
                    if model_field and model_field in data and data[model_field] is not None:
                        # Fill the field with data
                        value = str(data[model_field])
                        logger.debug(f"Filling field {field_name} with value: {value}")
                        
                        # Set the field value
                        annotation.V = f"({value})"
                        annotation.AP = ""  # Remove appearance stream to force regeneration
                        
                        # Set the field as modified
                        annotation[PdfName.Ff] = 1
                    else:
                        # Field is missing or None, use N/A as fallback
                        logger.debug(f"Missing field {model_field}, using N/A")
                        annotation.V = "(N/A)"
                        annotation.AP = ""  # Remove appearance stream to force regeneration
                        
                        if model_field:
                            missing_fields.append(model_field)
    
    # Write the filled PDF
    writer = PdfWriter()
    writer.write(output_path, template)
    
    logger.info(f"PDF generated successfully at: {output_path}")
    return missing_fields

def extract_application_data(application: Application) -> Dict[str, Any]:
    """
    Extract data from an Application instance and its related models.
    
    Args:
        application: The Application instance to extract data from
        
    Returns:
        A dictionary mapping model field names to values
    """
    data = {
        # Application fields
        "reference_number": application.reference_number,
        "loan_amount": application.loan_amount,
        "loan_term": application.loan_term,
        "interest_rate": application.interest_rate,
        "loan_purpose": application.get_loan_purpose_display() if application.loan_purpose else None,
        "exit_strategy": application.get_exit_strategy_display() if application.exit_strategy else None,
        "additional_comments": application.additional_comments,
        "repayment_frequency": application.get_repayment_frequency_display() if application.repayment_frequency else None,
        "security_address": application.security_address,
        "security_type": application.security_type,
        "security_value": application.security_value,
    }
    
    # Get borrower information
    borrowers = application.borrowers.all()
    if borrowers.exists():
        # Process individual borrower (first non-company borrower)
        individual_borrower = borrowers.filter(is_company=False).first()
        if individual_borrower:
            data.update({
                "borrower_first_name": individual_borrower.first_name,
                "borrower_last_name": individual_borrower.last_name,
                "borrower_email": individual_borrower.email,
                "borrower_phone": individual_borrower.phone,
                "borrower_residential_address": individual_borrower.residential_address,
                "borrower_annual_income": individual_borrower.annual_income,
            })
        
        # Process company borrower (first company borrower)
        company_borrower = borrowers.filter(is_company=True).first()
        if company_borrower:
            data.update({
                "company_name": company_borrower.company_name,
                "company_abn": company_borrower.company_abn,
                "company_acn": company_borrower.company_acn,
                "company_address": company_borrower.company_address or format_registered_address(company_borrower),
                "annual_company_income": company_borrower.annual_company_income,
            })
    
    # Get loan requirement information
    loan_requirements = application.loan_requirements.all()
    if loan_requirements.exists():
        loan_requirement = loan_requirements.first()
        data.update({
            "loan_requirement_description": loan_requirement.description,
            "loan_requirement_amount": loan_requirement.amount,
        })
    
    # Get security property information
    security_properties = application.security_properties.all()
    if security_properties.exists():
        security_property = security_properties.first()
        data.update({
            "security_address": format_property_address(security_property),
            "security_type": security_property.get_property_type_display() if security_property.property_type else None,
            "security_value": security_property.estimated_value,
        })
    
    return data

def format_property_address(security_property) -> Optional[str]:
    """Format a security property address into a single string"""
    address_parts = [
        security_property.address_unit,
        security_property.address_street_no,
        security_property.address_street_name,
        security_property.address_suburb,
        security_property.address_state,
        security_property.address_postcode
    ]
    address = ' '.join(filter(None, address_parts))
    return address if address else None

def format_registered_address(borrower) -> Optional[str]:
    """Format a borrower's registered address into a single string"""
    address_parts = [
        borrower.registered_address_unit,
        borrower.registered_address_street_no,
        borrower.registered_address_street_name,
        borrower.registered_address_suburb,
        borrower.registered_address_state,
        borrower.registered_address_postcode
    ]
    address = ' '.join(filter(None, address_parts))
    return address if address else None
