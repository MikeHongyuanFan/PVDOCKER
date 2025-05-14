import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

# Import models and functions
from applications.models import Application
from applications.utils.pdf_filler import fill_pdf_form
from django.conf import settings

def generate_pdf():
    # Get the first application
    app = Application.objects.first()
    
    if not app:
        print("No applications found in the database.")
        return
    
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
    generate_pdf()
