#!/bin/bash

# Script to generate OpenAPI schema files for the CRM Loan Management System

echo "Generating OpenAPI schema files..."

# Navigate to the Django project directory
cd backenddjango

# Generate YAML schema
echo "Generating YAML schema..."
python3 manage.py spectacular --file schema.yaml
echo "YAML schema generated at backenddjango/schema.yaml"

# Generate JSON schema
echo "Generating JSON schema..."
python3 manage.py spectacular --file schema.json --format openapi-json
echo "JSON schema generated at backenddjango/schema.json"

echo "Schema generation complete!"
echo ""
echo "API documentation is now available at:"
echo "- Swagger UI: http://localhost:8000/api/swagger/"
echo "- ReDoc: http://localhost:8000/api/redoc/"
echo "- Schema: http://localhost:8000/api/schema/"
