import os
import django
from pdfrw import PdfReader

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from django.conf import settings

def inspect_pdf_fields():
    """Inspect the PDF template to identify all form fields"""
    
    # Get the path to the template PDF
    template_path = os.path.join(
        settings.BASE_DIR, 
        'applications', 
        'ApplicationTemplate', 
        'Eternity Capital - Application Form (1).pdf'
    )
    
    if not os.path.exists(template_path):
        print(f"PDF template not found at {template_path}")
        return
    
    # Read the template PDF
    template = PdfReader(template_path)
    
    # Dictionary to store field information
    fields = {}
    
    # Inspect all pages for form fields
    for i, page in enumerate(template.pages):
        print(f"\nPage {i+1}:")
        
        if page.Annots:
            for j, annotation in enumerate(page.Annots):
                if annotation.FT:
                    field_type = annotation.FT
                    field_name = annotation.T if hasattr(annotation, 'T') else f"Unknown_{i}_{j}"
                    
                    # Store field information
                    fields[field_name] = {
                        'type': field_type,
                        'page': i+1,
                        'properties': {}
                    }
                    
                    # Extract additional properties
                    for prop in dir(annotation):
                        if not prop.startswith('_') and prop not in ['FT', 'T']:
                            value = getattr(annotation, prop)
                            if value:
                                fields[field_name]['properties'][prop] = str(value)
                    
                    print(f"  Field: {field_name}, Type: {field_type}")
                    for prop, value in fields[field_name]['properties'].items():
                        print(f"    {prop}: {value}")
    
    # Print summary
    print(f"\nTotal fields found: {len(fields)}")
    print("Field names:")
    for name in sorted(fields.keys()):
        print(f"  {name}")
    
    return fields

if __name__ == "__main__":
    inspect_pdf_fields()
