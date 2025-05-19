#!/usr/bin/env python
"""
Enhanced Serializer Schema Extractor

This script recursively walks through a Django REST Framework serializer class
and outputs a detailed JSON-style dictionary with comprehensive field information including:
- Field name
- Field type (e.g., CharField, DecimalField)
- Whether it's required (required: true/false)
- Whether it's read-only
- Default value (if any)
- Help text (if defined)
- Label (if defined)
- Max/min length for text fields
- Max/min value for numeric fields
- Choices list for ChoiceField
- Nested children fields for nested serializers or lists
- Notes on many=True relationships

Usage:
    python tools/serializer_schema_extractor_enhanced.py

Example output:
{
  "reference_number": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "max_length": 100,
    "help_text": "Unique reference number for the application"
  },
  "borrowers": {
    "type": "ListSerializer",
    "required": true,
    "read_only": false,
    "many": true,
    "children": {
      "first_name": {
        "type": "CharField",
        "required": true,
        "read_only": false,
        "max_length": 100
      },
      "email": {
        "type": "EmailField",
        "required": true,
        "read_only": false
      }
    }
  }
}
"""

import os
import sys
import json
import pprint
from collections import OrderedDict

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backenddjango'))

# Set up Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from rest_framework import serializers
from applications.serializers import ApplicationCreateSerializer


def get_field_type(field):
    """Get the field type name as a string."""
    return field.__class__.__name__


def is_serializer(field):
    """Check if a field is a serializer."""
    return isinstance(field, serializers.Serializer) or isinstance(field, serializers.ModelSerializer)


def is_list_serializer(field):
    """Check if a field is a list serializer."""
    return isinstance(field, serializers.ListSerializer) or (
        hasattr(field, 'child') and isinstance(field, serializers.ListField)
    )


def extract_field_metadata(field):
    """
    Extract detailed metadata from a field.
    
    Args:
        field: A DRF serializer field
        
    Returns:
        A dictionary with field metadata
    """
    metadata = {
        "type": get_field_type(field),
        "required": getattr(field, 'required', False),
        "read_only": getattr(field, 'read_only', False),
    }
    
    # Add default value if present and not empty
    default = getattr(field, 'default', None)
    if default is not None and default != serializers.empty:
        metadata["default"] = default
    
    # Add help text if present
    help_text = getattr(field, 'help_text', None)
    if help_text:
        metadata["help_text"] = help_text
    
    # Add label if present
    label = getattr(field, 'label', None)
    if label:
        metadata["label"] = label
    
    # Add max_length and min_length for string fields
    if hasattr(field, 'max_length') and field.max_length is not None:
        metadata["max_length"] = field.max_length
    if hasattr(field, 'min_length') and field.min_length is not None:
        metadata["min_length"] = field.min_length
    
    # Add max_value and min_value for numeric fields
    if hasattr(field, 'max_value') and field.max_value is not None:
        metadata["max_value"] = field.max_value
    if hasattr(field, 'min_value') and field.min_value is not None:
        metadata["min_value"] = field.min_value
    
    # Add choices for choice fields
    if hasattr(field, 'choices') and field.choices:
        # Convert choices to a dictionary for better readability
        if isinstance(field.choices, dict):
            metadata["choices"] = field.choices
        else:
            metadata["choices"] = dict(field.choices)
    
    return metadata


def extract_serializer_schema(serializer_instance):
    """
    Recursively extract detailed schema from a serializer instance.
    
    Args:
        serializer_instance: A DRF serializer instance
        
    Returns:
        A dictionary representing the serializer schema with detailed field information
    """
    result = {}
    
    # Get all fields from the serializer
    fields = getattr(serializer_instance, 'fields', {})
    
    for field_name, field in fields.items():
        # Handle SerializerMethodField
        if isinstance(field, serializers.SerializerMethodField):
            metadata = extract_field_metadata(field)
            result[field_name] = metadata
            continue
            
        # Handle nested serializers
        if is_serializer(field):
            nested_result = extract_serializer_schema(field)
            metadata = extract_field_metadata(field)
            metadata["children"] = nested_result
            result[field_name] = metadata
            continue
            
        # Handle list serializers (many=True)
        if is_list_serializer(field):
            child = field.child
            metadata = extract_field_metadata(field)
            metadata["many"] = True
            
            if is_serializer(child):
                nested_result = extract_serializer_schema(child)
                metadata["children"] = nested_result
            else:
                # For ListField with simple types, add child field metadata
                child_metadata = extract_field_metadata(child)
                metadata["child_type"] = child_metadata
                
            result[field_name] = metadata
            continue
            
        # Handle regular fields
        metadata = extract_field_metadata(field)
        result[field_name] = metadata
            
    return result


def main():
    """Main function to extract and print serializer schema."""
    # Create an instance of the serializer without data
    serializer = ApplicationCreateSerializer()
    
    # Extract detailed schema
    schema = extract_serializer_schema(serializer)
    
    # Print the schema using pprint for better formatting
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(schema)
    
    # Save the schema to a JSON file
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'application_schema_enhanced.json')
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print(f"\nSchema saved to {output_path}")


if __name__ == "__main__":
    main()
