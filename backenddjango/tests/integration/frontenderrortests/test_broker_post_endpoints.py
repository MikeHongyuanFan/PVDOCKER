"""
Integration tests specifically for the POST endpoints for branches and BDMs
that are reportedly returning 405 Method Not Allowed errors.

This test will:
1. Test POST requests to /api/brokers/branches/ and /api/brokers/bdms/
2. Diagnose why these endpoints might be returning 405 errors
3. Test alternative request formats and content types
4. Provide detailed error information
"""

import pytest
import json
import logging
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from brokers.models import Branch, BDM, Broker

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()

@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    user = User.objects.create_user(
        username='admin_test',
        email='admin@example.com',
        password='adminpassword',
        role='admin'
    )
    return user

@pytest.fixture
def test_branch(db):
    """Create and return a test branch."""
    branch = Branch.objects.create(
        name="Test Branch",
        address="123 Test St",
        phone="1234567890",
        email="branch@example.com"
    )
    return branch

@pytest.fixture
def test_broker(db):
    """Create and return a test broker."""
    broker = Broker.objects.create(
        name="Test Broker",
        company="Test Company",
        email="broker@example.com",
        phone="0987654321"
    )
    return broker

@pytest.mark.django_db
class TestBrokerPostEndpoints:
    """Test class specifically for the broker POST endpoints."""
    
    def test_post_branch_endpoint(self, client, admin_user):
        """Test POST request to /api/brokers/branches/ endpoint."""
        # Login as admin
        client.force_login(admin_user)
        
        # Prepare branch data
        branch_data = {
            "name": "New Test Branch",
            "address": "456 New Branch St",
            "phone": "5551234567",
            "email": "newbranch@example.com"
        }
        
        # Test POST request
        url = '/api/brokers/branches/'
        response = client.post(
            url,
            data=json.dumps(branch_data),
            content_type='application/json'
        )
        
        # Log detailed information about the response
        logger.info(f"POST to {url} returned status code: {response.status_code}")
        logger.info(f"Response content: {response.content.decode('utf-8')}")
        
        if response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            # If we get a 405, try to diagnose the issue
            logger.error("Received 405 Method Not Allowed. Checking allowed methods...")
            allowed_methods = response.get('Allow', '')
            logger.info(f"Allowed methods: {allowed_methods}")
            
            # Try to get the URL pattern that matched this request
            from django.urls.resolvers import get_resolver
            resolver = get_resolver()
            possible_patterns = resolver.resolve(url.lstrip('/'))
            logger.info(f"URL pattern that matched: {possible_patterns}")
            
            # Check if the viewset has create method
            try:
                from brokers.views import BranchViewSet
                logger.info(f"BranchViewSet has create method: {hasattr(BranchViewSet, 'create')}")
                logger.info(f"BranchViewSet actions: {getattr(BranchViewSet, 'http_method_names', [])}")
            except ImportError:
                logger.error("Could not import BranchViewSet")
        
        # Try with trailing slash removed if it failed
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            url_no_slash = url.rstrip('/')
            logger.info(f"Trying without trailing slash: {url_no_slash}")
            response_no_slash = client.post(
                url_no_slash,
                data=json.dumps(branch_data),
                content_type='application/json'
            )
            logger.info(f"POST to {url_no_slash} returned status code: {response_no_slash.status_code}")
        
        # Try with form data instead of JSON
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            logger.info(f"Trying with form data instead of JSON")
            response_form = client.post(url, data=branch_data)
            logger.info(f"POST with form data to {url} returned status code: {response_form.status_code}")
        
        # Assert that one of our attempts should have worked
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK] or \
               (response_no_slash.status_code if 'response_no_slash' in locals() else 0) in [status.HTTP_201_CREATED, status.HTTP_200_OK] or \
               (response_form.status_code if 'response_form' in locals() else 0) in [status.HTTP_201_CREATED, status.HTTP_200_OK], \
               f"All POST attempts to branch endpoint failed"
    
    def test_post_bdm_endpoint(self, client, admin_user, test_branch):
        """Test POST request to /api/brokers/bdms/ endpoint."""
        # Login as admin
        client.force_login(admin_user)
        
        # Prepare BDM data
        bdm_data = {
            "name": "New Test BDM",
            "email": "newbdm@example.com",
            "phone": "5559876543",
            "branch_id": test_branch.id
        }
        
        # Test POST request
        url = '/api/brokers/bdms/'
        response = client.post(
            url,
            data=json.dumps(bdm_data),
            content_type='application/json'
        )
        
        # Log detailed information about the response
        logger.info(f"POST to {url} returned status code: {response.status_code}")
        logger.info(f"Response content: {response.content.decode('utf-8')}")
        
        if response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            # If we get a 405, try to diagnose the issue
            logger.error("Received 405 Method Not Allowed. Checking allowed methods...")
            allowed_methods = response.get('Allow', '')
            logger.info(f"Allowed methods: {allowed_methods}")
            
            # Try to get the URL pattern that matched this request
            from django.urls.resolvers import get_resolver
            resolver = get_resolver()
            possible_patterns = resolver.resolve(url.lstrip('/'))
            logger.info(f"URL pattern that matched: {possible_patterns}")
            
            # Check if the viewset has create method
            try:
                from brokers.views import BDMViewSet
                logger.info(f"BDMViewSet has create method: {hasattr(BDMViewSet, 'create')}")
                logger.info(f"BDMViewSet actions: {getattr(BDMViewSet, 'http_method_names', [])}")
            except ImportError:
                logger.error("Could not import BDMViewSet")
        
        # Try with trailing slash removed if it failed
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            url_no_slash = url.rstrip('/')
            logger.info(f"Trying without trailing slash: {url_no_slash}")
            response_no_slash = client.post(
                url_no_slash,
                data=json.dumps(bdm_data),
                content_type='application/json'
            )
            logger.info(f"POST to {url_no_slash} returned status code: {response_no_slash.status_code}")
        
        # Try with form data instead of JSON
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            logger.info(f"Trying with form data instead of JSON")
            response_form = client.post(url, data=bdm_data)
            logger.info(f"POST with form data to {url} returned status code: {response_form.status_code}")
        
        # Try the special create_with_branch endpoint
        if response.status_code not in [status.HTTP_201_CREATED, status.HTTP_200_OK]:
            special_url = '/api/brokers/bdms/create_with_branch/'
            logger.info(f"Trying special endpoint: {special_url}")
            special_data = bdm_data.copy()
            special_data.pop('branch_id', None)
            special_data.update({
                "branch_name": "New Branch for BDM",
                "address": "789 BDM Branch St",
                "branch_phone": "5551112222",
                "branch_email": "bdmbranch@example.com"
            })
            response_special = client.post(
                special_url,
                data=json.dumps(special_data),
                content_type='application/json'
            )
            logger.info(f"POST to {special_url} returned status code: {response_special.status_code}")
        
        # Assert that one of our attempts should have worked
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK] or \
               (response_no_slash.status_code if 'response_no_slash' in locals() else 0) in [status.HTTP_201_CREATED, status.HTTP_200_OK] or \
               (response_form.status_code if 'response_form' in locals() else 0) in [status.HTTP_201_CREATED, status.HTTP_200_OK] or \
               (response_special.status_code if 'response_special' in locals() else 0) in [status.HTTP_201_CREATED, status.HTTP_200_OK], \
               f"All POST attempts to BDM endpoint failed"
    
    def test_get_branch_endpoint(self, client, admin_user):
        """Test GET request to /api/brokers/branches/ endpoint to verify it works."""
        # Login as admin
        client.force_login(admin_user)
        
        # Test GET request
        url = '/api/brokers/branches/'
        response = client.get(url)
        
        # Log detailed information about the response
        logger.info(f"GET to {url} returned status code: {response.status_code}")
        
        # Assert that GET works
        assert response.status_code == status.HTTP_200_OK, f"GET request to branch endpoint failed"
    
    def test_get_bdm_endpoint(self, client, admin_user):
        """Test GET request to /api/brokers/bdms/ endpoint to verify it works."""
        # Login as admin
        client.force_login(admin_user)
        
        # Test GET request
        url = '/api/brokers/bdms/'
        response = client.get(url)
        
        # Log detailed information about the response
        logger.info(f"GET to {url} returned status code: {response.status_code}")
        
        # Assert that GET works
        assert response.status_code == status.HTTP_200_OK, f"GET request to BDM endpoint failed"
    
    def test_options_branch_endpoint(self, client):
        """Test OPTIONS request to /api/brokers/branches/ endpoint to check allowed methods."""
        # Test OPTIONS request
        url = '/api/brokers/branches/'
        response = client.options(url)
        
        # Log detailed information about the response
        logger.info(f"OPTIONS to {url} returned status code: {response.status_code}")
        logger.info(f"Allow header: {response.get('Allow', '')}")
        
        # Check if POST is in the allowed methods
        allowed_methods = response.get('Allow', '')
        assert 'POST' in allowed_methods, f"POST is not in allowed methods: {allowed_methods}"
    
    def test_options_bdm_endpoint(self, client):
        """Test OPTIONS request to /api/brokers/bdms/ endpoint to check allowed methods."""
        # Test OPTIONS request
        url = '/api/brokers/bdms/'
        response = client.options(url)
        
        # Log detailed information about the response
        logger.info(f"OPTIONS to {url} returned status code: {response.status_code}")
        logger.info(f"Allow header: {response.get('Allow', '')}")
        
        # Check if POST is in the allowed methods
        allowed_methods = response.get('Allow', '')
        assert 'POST' in allowed_methods, f"POST is not in allowed methods: {allowed_methods}"
