from django.template.loader import render_to_string
from django.conf import settings
import os
from uuid import uuid4
from django.utils import timezone
from weasyprint import HTML
from .models import Document


def generate_document_from_template(template_name, context, output_filename, document_type, application, user):
    """
    Generate a document from a template
    
    Args:
        template_name: Name of the template file
        context: Context data for the template
        output_filename: Name for the output file
        document_type: Type of document being generated
        application: Application object
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    # Generate HTML content
    html_content = render_to_string(template_name, context)
    
    # Generate PDF
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents', str(application.id))
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_filename}_{uuid.uuid4().hex}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    HTML(string=html_content).write_pdf(output_path)
    
    # Create document record
    relative_path = os.path.join('generated_documents', str(application.id), filename)
    
    document = Document.objects.create(
        title=output_filename,
        document_type=document_type,
        file=relative_path,
        file_name=filename,
        file_size=os.path.getsize(output_path),
        file_type='application/pdf',
        application=application,
        created_by=user
    )
    
    return document


def generate_guarantor_letter(guarantor_id, user):
    """
    Generate a guarantor letter
    
    Args:
        guarantor_id: ID of the guarantor
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    from borrowers.models import Guarantor
    
    try:
        guarantor = Guarantor.objects.get(id=guarantor_id)
    except Guarantor.DoesNotExist:
        return None
    
    application = guarantor.application
    
    # Generate context
    context = {
        'guarantor': guarantor,
        'application': application,
        'borrower': guarantor.borrower,
        'generated_date': timezone.now().strftime('%d/%m/%Y'),
    }
    
    # Generate document
    template_name = 'documents/guarantor_letter.html'
    output_filename = f"Guarantor_Letter_{guarantor.id}"
    
    return generate_document_from_template(
        template_name=template_name,
        context=context,
        output_filename=output_filename,
        document_type='guarantor_letter',
        application=application,
        user=user
    )


def generate_company_borrower_documents(borrower_id, user):
    """
    Generate company borrower specific documents
    
    Args:
        borrower_id: ID of the company borrower
        user: User generating the document
        
    Returns:
        List of Document objects if successful, empty list otherwise
    """
    from borrowers.models import Borrower
    
    try:
        borrower = Borrower.objects.get(id=borrower_id, is_company=True)
    except Borrower.DoesNotExist:
        return []
    
    # Get the first application for this borrower
    application = borrower.applications.first()
    if not application:
        return []
    
    documents = []
    
    # Generate company declaration
    context = {
        'borrower': borrower,
        'application': application,
        'generated_date': timezone.now().strftime('%d/%m/%Y'),
    }
    
    company_declaration = generate_document_from_template(
        template_name='documents/company_declaration.html',
        context=context,
        output_filename=f"Company_Declaration_{borrower.id}",
        document_type='company_declaration',
        application=application,
        user=user
    )
    
    if company_declaration:
        documents.append(company_declaration)
    
    # Generate director's guarantee
    director_guarantee = generate_document_from_template(
        template_name='documents/director_guarantee.html',
        context=context,
        output_filename=f"Director_Guarantee_{borrower.id}",
        document_type='director_guarantee',
        application=application,
        user=user
    )
    
    if director_guarantee:
        documents.append(director_guarantee)
    
    return documents
