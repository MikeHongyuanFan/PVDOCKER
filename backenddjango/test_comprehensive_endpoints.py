#!/usr/bin/env python
"""
Standalone script to test the existence of all URL endpoints in the Django application,
including sub-URLs for each main endpoint.
"""

import requests
import sys
from urllib.parse import urljoin
import json
from collections import defaultdict

def test_comprehensive_endpoints(base_url="http://localhost:8000"):
    """
    Test if all endpoints exist by making HTTP requests.
    
    Args:
        base_url: The base URL of the Django application
    """
    # Define all endpoints to test, organized by module
    endpoints = {
        'admin': [
            '/admin/',
        ],
        'api_docs': [
            '/api/schema/',
            '/api/swagger/',
            '/api/redoc/',
        ],
        'users': [
            '/api/users/',
            '/api/users/auth/login/',
            '/api/users/auth/logout/',
            '/api/users/auth/register/',
            '/api/users/auth/refresh/',
            '/api/users/auth/reset-password-request/',
            '/api/users/auth/reset-password-confirm/',
            '/api/users/profile/',
            '/api/users/profile/update/',
            '/api/users/notifications/',
            '/api/users/notifications/mark-read/',
            '/api/users/notifications/count/',
            '/api/users/notification-preferences/',
            '/api/users/users/',
            '/api/users/notifications-viewset/',
        ],
        'applications': [
            '/api/applications/',
            '/api/applications/enhanced-applications/',
            '/api/applications/create-with-cascade/',
            '/api/applications/validate-schema/',
            '/api/applications/manual-funding-calculator/',
            # The following endpoints require an application ID
            '/api/applications/1/signature/',
            '/api/applications/1/stage/',
            '/api/applications/1/borrowers/',
            '/api/applications/1/sign/',
            '/api/applications/1/extend-loan/',
            '/api/applications/1/funding-calculation/',
            '/api/applications/1/funding-calculation-history/',
            '/api/applications/1/generate-pdf/',
        ],
        'borrowers': [
            '/api/borrowers/',
            '/api/borrowers/guarantors/',
            '/api/borrowers/borrowers/',
            # The following endpoints require IDs
            '/api/borrowers/borrowers/1/assets/',
            '/api/borrowers/guarantors/1/assets/',
        ],
        'brokers': [
            '/api/brokers/',
            '/api/brokers/bdms/',
            '/api/brokers/branches/',
        ],
        'documents': [
            '/api/documents/',
            '/api/documents/documents/',
            '/api/documents/notes/',
            '/api/documents/fees/',
            '/api/documents/repayments/',
            '/api/documents/note-comments/',
            # The following endpoints require IDs
            '/api/documents/documents/1/create-version/',
            '/api/documents/fees/1/mark-paid/',
            '/api/documents/repayments/1/mark-paid/',
            '/api/documents/applications/1/ledger/',
        ],
        'products': [
            '/api/products/',
            '/api/products/products/',
        ],
        'reports': [
            '/api/reports/repayment-compliance/',
            '/api/reports/application-volume/',
            '/api/reports/application-status/',
        ],
    }
    
    # Flatten the endpoints dictionary into a single list
    all_endpoints = [endpoint for category in endpoints.values() for endpoint in category]
    
    results = defaultdict(list)
    success_count = 0
    failure_count = 0
    
    print(f"Testing {len(all_endpoints)} endpoints against {base_url}...")
    print("-" * 60)
    
    for endpoint in all_endpoints:
        url = urljoin(base_url, endpoint)
        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            
            # We consider any response other than 404 as a success
            # (the endpoint exists, even if it requires authentication)
            if status_code != 404:
                result = f"✅ {endpoint} - Status: {status_code}"
                results['success'].append(result)
                success_count += 1
            else:
                result = f"❌ {endpoint} - Status: 404 Not Found"
                results['failure'].append(result)
                failure_count += 1
        except requests.RequestException as e:
            result = f"❌ {endpoint} - Error: {str(e)}"
            results['error'].append(result)
            failure_count += 1
        
        print(result)
    
    print("-" * 60)
    print(f"Summary: {success_count} endpoints exist, {failure_count} failed")
    
    # Print failures by category
    if results['failure'] or results['error']:
        print("\nFailed endpoints:")
        for failure in results['failure'] + results['error']:
            print(f"  {failure}")
    
    return success_count, failure_count, results

if __name__ == "__main__":
    # Allow specifying a custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    success, failure, _ = test_comprehensive_endpoints(base_url)
    
    # Exit with non-zero status if any endpoints failed
    sys.exit(1 if failure > 0 else 0)
