import os
import django
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

# Import models and functions
from applications.models import Application
from applications.utils.pdf_filler import fill_pdf_form
from django.conf import settings
from borrowers.models import Borrower
from users.models import User
from django.utils import timezone

def create_enhanced_application():
    """Create or update an application with comprehensive mock data"""
    
    # Get or create a user for the application
    user, _ = User.objects.get_or_create(
        username="mockuser",
        defaults={
            "email": "mock@example.com",
            "first_name": "Mock",
            "last_name": "User",
            "role": "admin"
        }
    )
    
    # Create an individual borrower with complete information
    individual_borrower, _ = Borrower.objects.get_or_create(
        email="john.smith@example.com",
        defaults={
            "first_name": "John",
            "last_name": "Smith",
            "phone": "0412345678",
            "residential_address": "42 Main Street, Sydney NSW 2000",
            "annual_income": Decimal("120000.00"),
            "employment_type": "full_time",
            "employer_name": "Tech Solutions Inc.",
            "employment_duration": 36,  # 3 years in months
            "created_by": user
        }
    )
    
    # Create a company borrower with complete information
    company_borrower, _ = Borrower.objects.get_or_create(
        company_name="Acme Corporation Pty Ltd",
        defaults={
            "is_company": True,
            "company_abn": "12345678901",
            "company_acn": "123456789",
            "company_address": "100 Business Park Drive, Melbourne VIC 3000",
            "annual_company_income": Decimal("1500000.00"),
            "created_by": user
        }
    )
    
    # Create or update an application with comprehensive information
    app, created = Application.objects.get_or_create(
        reference_number="APP-MOCK-2025",
        defaults={
            "loan_amount": Decimal("750000.00"),
            "loan_term": 36,  # 3 years
            "interest_rate": Decimal("5.75"),
            "loan_purpose": "purchase",
            "exit_strategy": "sale",
            "additional_comments": "This is a comprehensive mock application for testing PDF generation",
            "repayment_frequency": "monthly",
            "security_address": "123 Investment Property, Brisbane QLD 4000",
            "security_type": "residential",
            "security_value": Decimal("950000.00"),
            "created_by": user
        }
    )
    
    # If we're updating an existing application, update its fields
    if not created:
        app.loan_amount = Decimal("750000.00")
        app.loan_term = 36
        app.interest_rate = Decimal("5.75")
        app.loan_purpose = "purchase"
        app.exit_strategy = "sale"
        app.additional_comments = "This is a comprehensive mock application for testing PDF generation"
        app.repayment_frequency = "monthly"
        app.security_address = "123 Investment Property, Brisbane QLD 4000"
        app.security_type = "residential"
        app.security_value = Decimal("950000.00")
        app.save()
    
    # Clear existing borrowers and add our new ones
    app.borrowers.clear()
    app.borrowers.add(individual_borrower, company_borrower)
    
    print(f"{'Created' if created else 'Updated'} application with ID: {app.id}")
    return app

def generate_pdf(app):
    """Generate a PDF for the given application"""
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(settings.MEDIA_ROOT, 'application_forms')
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output path
    output_path = os.path.join(output_dir, f'{app.id}_filled.pdf')
    
    try:
        # Fill the PDF form
        missing_fields = fill_pdf_form(app, output_path)
        
        print(f"PDF generated successfully at: {output_path}")
        print(f"Missing fields: {missing_fields}")
        
        # Return the path for convenience
        return output_path
    
    except FileNotFoundError as e:
        print(f"Error: PDF template not found - {str(e)}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    # Create enhanced application with mock data
    app = create_enhanced_application()
    
    # Generate PDF with the enhanced application
    generate_pdf(app)
