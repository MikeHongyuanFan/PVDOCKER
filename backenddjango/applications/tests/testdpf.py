#!/usr/bin/env python
"""
Test PDF Generation Script
Uses the PDF filler to generate a filled PDF with application data
"""

import os
import sys
import django
from datetime import datetime, date
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from applications.models import Application, SecurityProperty, LoanRequirement
from borrowers.models import Borrower, Guarantor
from django.contrib.auth import get_user_model
from applications.utils.pdf_filler import fill_pdf_form

User = get_user_model()

def create_sample_application():
    """Create a sample application with comprehensive test data"""
    
    print("Creating sample application with test data...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Create the main application
    application = Application.objects.create(
        created_by=user,
        reference_number="APP-2025-001",
        loan_amount=Decimal('500000.00'),
        loan_term=12,  # 12 months
        interest_rate=Decimal('8.50'),
        application_type="residential",
        loan_purpose="purchase",
        exit_strategy="sale",
        repayment_frequency="monthly",
        estimated_settlement_date=date(2025, 8, 15),
        signed_by="John Smith",
        signature_date=date.today(),
        additional_comments="Test application for PDF generation",
        
        # Valuer information
        valuer_company_name="Elite Property Valuers",
        valuer_contact_name="Sarah Johnson",
        valuer_phone="02 9123 4567",
        valuer_email="sarah@elitevaluers.com.au",
        valuation_date=date(2025, 6, 10),
        valuation_amount=Decimal('520000.00'),
        
        # Quantity Surveyor information
        qs_company_name="Premier QS Services",
        qs_contact_name="Michael Brown",
        qs_phone="02 9876 5432",
        qs_email="michael@premierqs.com.au",
        qs_report_date=date(2025, 6, 5),
        
        # Solvency enquiries
        has_pending_litigation=False,
        has_unsatisfied_judgements=False,
        has_been_bankrupt=False,
        has_been_refused_credit=False,
        has_outstanding_ato_debt=False,
        has_outstanding_tax_returns=False,
        has_payment_arrangements=False,
        prior_application=False,
        solvency_enquiries_details="No adverse credit history"
    )
    
    print(f"Created application: {application.reference_number}")
    
    # Create individual borrower
    individual_borrower = Borrower.objects.create(
        is_company=False,
        first_name="John",
        last_name="Smith",
        date_of_birth=date(1985, 3, 15),
        email="john.smith@email.com",
        phone="02 9111 2222",
        residential_address="123 Main Street, Sydney NSW 2000",
        
        # Employment details
        job_title="Software Engineer",
        employer_name="Tech Solutions Pty Ltd",
        employment_type="full_time",
        annual_income=Decimal('95000.00'),
        employment_duration=36,  # 3 years in months
        employer_address="Level 10, 456 Business Street, Sydney NSW 2000",
        
        # Financial details
        monthly_expenses=Decimal('3500.00'),
        other_income=Decimal('5000.00'),
        tax_id="123456789",
        marital_status="married",
        
        # Bank details
        bank_name="Commonwealth Bank",
        bank_account_number="123456789",
        
        # Created by
        created_by=user
    )
    
    print(f"Created individual borrower: {individual_borrower.first_name} {individual_borrower.last_name}")
    
    # Create company borrower
    company_borrower = Borrower.objects.create(
        is_company=True,
        company_name="Smith Holdings Pty Ltd",
        company_abn="12 345 678 901",
        company_acn="123 456 789",
        contact_number="02 9333 4444",
        annual_company_income=Decimal('150000.00'),
        industry_type="technology",
        is_trustee=False,
        is_smsf_trustee=False,
        
        # Registered address
        registered_address_unit="Suite 5",
        registered_address_street_no="789",
        registered_address_street_name="Corporate Drive",
        registered_address_suburb="North Sydney",
        registered_address_state="NSW",
        registered_address_postcode="2060",
        company_address="Suite 5, 789 Corporate Drive, North Sydney NSW 2060",
        
        # Created by
        created_by=user
    )
    
    print(f"Created company borrower: {company_borrower.company_name}")
    
    # Add borrowers to application
    application.borrowers.add(individual_borrower, company_borrower)
    
    # Create individual guarantor
    individual_guarantor = Guarantor.objects.create(
        application=application,
        guarantor_type="individual",
        title="mr",
        first_name="Robert",
        last_name="Johnson",
        date_of_birth=date(1960, 7, 20),
        drivers_licence_no="12345678",
        email="robert.johnson@email.com",
        home_phone="02 9555 6666",
        mobile="0423 456 789",
        
        # Address
        address_unit="Apt 2",
        address_street_no="456",
        address_street_name="Guarantor Street",
        address_suburb="Bondi",
        address_state="NSW",
        address_postcode="2026",
        
        # Employment
        occupation="Business Manager",
        employer_name="Finance Corp Ltd",
        employment_type="full_time",
        annual_income=Decimal('85000.00')
    )
    
    print(f"Created individual guarantor: {individual_guarantor.first_name} {individual_guarantor.last_name}")
    
    # Create security property
    security_property = SecurityProperty.objects.create(
        application=application,
        
        # Address
        address_unit="Unit 12",
        address_street_no="567",
        address_street_name="Property Lane",
        address_suburb="Surry Hills",
        address_state="NSW",
        address_postcode="2010",
        
        # Property details
        property_type="residential",
        estimated_value=Decimal('520000.00'),
        purchase_price=Decimal('500000.00'),
        bedrooms=2,
        bathrooms=2,
        car_spaces=1,
        building_size=Decimal('85.0'),
        land_size=Decimal('120.0'),
        
        # Features
        is_single_story=False,
        has_garage=True,
        has_carport=False,
        has_off_street_parking=True,
        occupancy="owner_occupied",
        
        # Mortgage details
        current_mortgagee="Bank of Australia",
        first_mortgage="250000.00",
        second_mortgage="0.00",
        current_debt_position=Decimal('250000.00'),
        
        # Created by
        created_by=user
    )
    
    print(f"Created security property: {security_property.address_street_no} {security_property.address_street_name}")
    
    # Create loan requirement
    loan_requirement = LoanRequirement.objects.create(
        application=application,
        description="Purchase of residential property with minor renovations",
        amount=Decimal('500000.00'),
        created_by=user
    )
    
    print(f"Created loan requirement: {loan_requirement.description}")
    
    # Add guarantor to application
    application.guarantors.add(individual_guarantor)
    
    return application

def get_existing_application():
    """Get an existing application from the database"""
    
    try:
        # Try to get the most recent application
        application = Application.objects.latest('created_at')
        print(f"Using existing application: {application.reference_number}")
        return application
    except Application.DoesNotExist:
        print("No existing applications found.")
        return None

def generate_pdf_with_data(application, output_filename="filled_application_form.pdf"):
    """Generate a filled PDF using the application data"""
    
    output_dir = "applications/ApplicationTemplate"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"\nGenerating PDF...")
    print(f"Application: {application.reference_number}")
    print(f"Output path: {output_path}")
    
    try:
        # Use the PDF filler to generate the filled form
        missing_fields = fill_pdf_form(application, output_path)
        
        print(f"\n✅ PDF generated successfully!")
        print(f"📁 Location: {output_path}")
        
        if missing_fields:
            print(f"\n⚠️  Missing data for {len(missing_fields)} fields:")
            for field in missing_fields[:10]:  # Show first 10 missing fields
                print(f"   - {field}")
            if len(missing_fields) > 10:
                print(f"   ... and {len(missing_fields) - 10} more")
        else:
            print("\n✅ All mapped fields were filled successfully!")
        
        # Get file size
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"📊 File size: {file_size_mb:.2f} MB")
        
        return output_path
        
    except Exception as e:
        print(f"\n❌ Error generating PDF: {str(e)}")
        raise

def main():
    """Main function"""
    print("PDF Generation Test Script")
    print("=" * 50)
    
    try:
        # Try to use existing application first
        application = get_existing_application()
        
        if not application:
            # Create sample application if none exists
            print("Creating sample application...")
            application = create_sample_application()
        
        # Generate PDF with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"filled_application_form_{timestamp}.pdf"
        
        # Generate the filled PDF
        pdf_path = generate_pdf_with_data(application, output_filename)
        
        print(f"\n{'='*50}")
        print("PDF GENERATION COMPLETE")
        print(f"{'='*50}")
        print(f"Application Reference: {application.reference_number}")
        print(f"Generated PDF: {pdf_path}")
        print("\nYou can now:")
        print("1. Open the PDF to review the filled form")
        print("2. Compare with the PNG image to verify field positions")
        print("3. Update mappings in pdf_filler.py if needed")
        
    except Exception as e:
        print(f"\n❌ Script failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 
