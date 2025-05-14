"""
Test script to investigate 404 errors reported by the frontend team.
This script tests the following endpoints:
- /api/borrowers/guarantors/ (GET)
- /api/brokers/bdms/ (GET)
- /api/brokers/branches/ (GET)

The script will:
1. Check if the endpoints exist
2. Check if the endpoints return the expected status code
3. Check if the endpoints return the expected data structure
4. Provide diagnostic information for any failures
"""

import pytest
import json
import logging
from django.urls import reverse, resolve, NoReverseMatch
from rest_framework import status
from django.urls.exceptions import Resolver404

# Set up logging
logger = logging.getLogger(__name__)

# List of endpoints to test
ENDPOINTS = [
    {
        'name': 'borrowers-guarantors',
        'url': '/api/borrowers/guarantors/',
        'method': 'GET',
        'expected_status': status.HTTP_200_OK,
    },
    {
        'name': 'brokers-bdms',
        'url': '/api/brokers/bdms/',
        'method': 'GET',
        'expected_status': status.HTTP_200_OK,
    },
    {
        'name': 'brokers-branches',
        'url': '/api/brokers/branches/',
        'method': 'GET',
        'expected_status': status.HTTP_200_OK,
    },
]

@pytest.mark.django_db
class TestFrontendErrors:
    """Test class for investigating frontend 404 errors."""

    def test_url_resolution(self):
        """Test if the URLs can be resolved by Django's URL resolver."""
        for endpoint in ENDPOINTS:
            try:
                # Try to resolve the URL
                resolver_match = resolve(endpoint['url'])
                logger.info(f"URL {endpoint['url']} resolves to {resolver_match.view_name}")
                assert resolver_match is not None, f"URL {endpoint['url']} could not be resolved"
            except Resolver404:
                logger.error(f"URL {endpoint['url']} could not be resolved")
                pytest.fail(f"URL {endpoint['url']} could not be resolved")

    def test_url_reverse(self):
        """Test if the URL names can be reversed."""
        # This is a more comprehensive test that checks if the URL names are correctly registered
        url_names = [
            'borrowers-guarantors-list',  # DRF default naming for viewsets
            'brokers-bdms-list',
            'brokers-branches-list',
        ]
        
        for name in url_names:
            try:
                url = reverse(name)
                logger.info(f"URL name '{name}' reverses to {url}")
            except NoReverseMatch:
                logger.warning(f"URL name '{name}' could not be reversed")
                # Try alternative naming conventions
                alternative_names = [
                    name.replace('-list', ''),
                    name.split('-')[0] + ':' + '-'.join(name.split('-')[1:]),
                ]
                for alt_name in alternative_names:
                    try:
                        url = reverse(alt_name)
                        logger.info(f"Alternative URL name '{alt_name}' reverses to {url}")
                        break
                    except NoReverseMatch:
                        continue
                else:
                    logger.error(f"No valid URL name found for {name}")

    @pytest.mark.parametrize('endpoint', ENDPOINTS)
    def test_endpoint_access(self, admin_client, endpoint):
        """Test if the endpoints can be accessed with admin credentials."""
        # Make the request
        response = admin_client.get(endpoint['url'])
        
        # Log the response details
        logger.info(f"Endpoint: {endpoint['url']}")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Content: {response.content.decode('utf-8')[:200]}...")
        
        # Check if the status code matches the expected status code
        if response.status_code != endpoint['expected_status']:
            logger.error(f"Expected status {endpoint['expected_status']}, got {response.status_code}")
            logger.error(f"Full response: {response.content.decode('utf-8')}")
            
            # Additional diagnostics for 404 errors
            if response.status_code == status.HTTP_404_NOT_FOUND:
                # Check if the app is registered in INSTALLED_APPS
                from django.conf import settings
                app_name = endpoint['url'].split('/')[2]  # Extract app name from URL
                if app_name in settings.INSTALLED_APPS:
                    logger.info(f"App '{app_name}' is registered in INSTALLED_APPS")
                else:
                    logger.error(f"App '{app_name}' is NOT registered in INSTALLED_APPS")
                
                # Check if the URL pattern is registered
                from django.urls import get_resolver
                resolver = get_resolver()
                patterns = resolver.url_patterns
                logger.info(f"Available URL patterns: {[p.pattern for p in patterns if hasattr(p, 'pattern')]}")
        
        # Assert the status code
        assert response.status_code == endpoint['expected_status'], \
            f"Expected status {endpoint['expected_status']}, got {response.status_code}"
        
        # If successful, check the response structure
        if response.status_code == status.HTTP_200_OK:
            try:
                data = json.loads(response.content)
                # Check if the response is a list or has a 'results' key (for paginated responses)
                assert isinstance(data, list) or 'results' in data, \
                    f"Expected a list or paginated response, got {type(data)}"
                logger.info(f"Response structure is valid")
            except json.JSONDecodeError:
                logger.error(f"Response is not valid JSON")
                pytest.fail(f"Response is not valid JSON")

    def test_url_patterns_inspection(self):
        """Inspect all URL patterns in the project to help diagnose issues."""
        from django.urls import get_resolver
        resolver = get_resolver()
        
        def get_patterns(resolver, prefix=''):
            patterns = []
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    # This is an include
                    patterns.extend(get_patterns(pattern, prefix + pattern.pattern.regex.pattern))
                else:
                    # This is a URL pattern
                    if hasattr(pattern, 'name') and pattern.name:
                        patterns.append({
                            'pattern': prefix + str(pattern.pattern),
                            'name': pattern.name,
                            'callback': pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback),
                        })
            return patterns
        
        all_patterns = get_patterns(resolver)
        
        # Log all URL patterns
        logger.info("All URL patterns in the project:")
        for pattern in all_patterns:
            logger.info(f"Pattern: {pattern['pattern']}, Name: {pattern['name']}, Callback: {pattern['callback']}")
        
        # Look for patterns that might match our problematic endpoints
        for endpoint in ENDPOINTS:
            url = endpoint['url']
            matching_patterns = [p for p in all_patterns if url.startswith(p['pattern']) or p['pattern'].startswith(url)]
            logger.info(f"Patterns that might match {url}:")
            for pattern in matching_patterns:
                logger.info(f"  {pattern}")
