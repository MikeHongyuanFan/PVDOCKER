#!/usr/bin/env python
"""
Serializer Inspector Tool

This script analyzes a Django REST Framework serializer and outputs its structure
as a JSON-style Python dictionary, showing field names, types, and nested serializers.

Usage:
    python tools/serializer_inspector.py

Example output:
{
  "reference_number": "CharField",
  "borrowers": [
    {
      "first_name": "CharField",
      "email": "EmailField"
    }
  ]
}
"""

import os
import sys
import json
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


def extract_serializer_fields(serializer_instance, include_required=False):
    """
    Recursively extract fields from a serializer instance.
    
    Args:
        serializer_instance: A DRF serializer instance
        include_required: Whether to include required field information
        
    Returns:
        A dictionary representing the serializer structure
    """
    result = {}
    
    # Get all fields from the serializer
    fields = getattr(serializer_instance, 'fields', {})
    
    for field_name, field in fields.items():
        # Handle SerializerMethodField
        if isinstance(field, serializers.SerializerMethodField):
            result[field_name] = "SerializerMethodField"
            continue
            
        # Handle nested serializers
        if is_serializer(field):
            nested_result = extract_serializer_fields(field, include_required)
            if include_required:
                result[field_name] = {
                    "type": get_field_type(field),
                    "required": field.required,
                    "fields": nested_result
                }
            else:
                result[field_name] = nested_result
            continue
            
        # Handle list serializers (many=True)
        if is_list_serializer(field):
            child = field.child
            if is_serializer(child):
                nested_result = extract_serializer_fields(child, include_required)
                if include_required:
                    result[field_name] = {
                        "type": "ListSerializer",
                        "required": field.required,
                        "child": nested_result
                    }
                else:
                    result[field_name] = [nested_result]
            else:
                # Handle ListField with simple types
                if include_required:
                    result[field_name] = {
                        "type": f"ListField({get_field_type(child)})",
                        "required": field.required
                    }
                else:
                    result[field_name] = f"ListField({get_field_type(child)})"
            continue
            
        # Handle regular fields
        if include_required:
            result[field_name] = {
                "type": get_field_type(field),
                "required": field.required
            }
        else:
            result[field_name] = get_field_type(field)
            
    return result


def main():
    """Main function to extract and print serializer structure."""
    # Create an instance of the serializer without data
    serializer = ApplicationCreateSerializer()
    
    # Extract fields with required information
    include_required = True  # Set to False if you don't want required info
    structure = extract_serializer_fields(serializer, include_required)
    
    # Print the structure as formatted JSON
    print(json.dumps(structure, indent=2))


if __name__ == "__main__":
    main()
