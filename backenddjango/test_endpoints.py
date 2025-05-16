#!/usr/bin/env python
"""
Script to test the existence of all URL endpoints in the Django application.
This script can be run directly without using the Django test framework.
"""

import requests
import sys
from urllib.parse import urljoin

def test_endpoints(base_url="http://localhost:8000"):
    """
    Test if all endpoints exist by making HTTP requests.
    
    Args:
        base_url: The base URL of the Django application
    """
    # List of endpoints to test
    endpoints = [
        '/admin/',
        '/api/users/',
        '/api/applications/',
        '/api/borrowers/',
        '/api/brokers/',
        '/api/documents/',
        '/api/products/',
        # Reports endpoint doesn't have a root endpoint, only specific report endpoints
        '/api/reports/repayment-compliance/',
        '/api/reports/application-volume/',
        '/api/reports/application-status/',
        '/api/schema/',
        '/api/swagger/',
        '/api/redoc/',
    ]
    
    results = []
    success_count = 0
    failure_count = 0
    
    print(f"Testing endpoints against {base_url}...")
    print("-" * 60)
    
    for endpoint in endpoints:
        url = urljoin(base_url, endpoint)
        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            
            # We consider any response other than 404 as a success
            # (the endpoint exists, even if it requires authentication)
            if status_code != 404:
                result = f"✅ {endpoint} - Status: {status_code}"
                success_count += 1
            else:
                result = f"❌ {endpoint} - Status: 404 Not Found"
                failure_count += 1
        except requests.RequestException as e:
            result = f"❌ {endpoint} - Error: {str(e)}"
            failure_count += 1
        
        print(result)
        results.append(result)
    
    print("-" * 60)
    print(f"Summary: {success_count} endpoints exist, {failure_count} failed")
    
    return success_count, failure_count, results

if __name__ == "__main__":
    # Allow specifying a custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    success, failure, _ = test_endpoints(base_url)
    
    # Exit with non-zero status if any endpoints failed
    sys.exit(1 if failure > 0 else 0)
