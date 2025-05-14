#!/bin/bash

# Script to run the PDF generation integration tests

# Change to the project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the tests with verbose output
echo "Running PDF generation integration tests..."
python manage.py test applications.tests.integration.test_pdf_generation -v 2

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All PDF generation tests passed!"
else
    echo "❌ Some tests failed. Please check the output above for details."
fi
