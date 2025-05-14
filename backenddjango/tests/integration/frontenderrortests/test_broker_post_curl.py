"""
Test script that uses subprocess to run curl commands against the broker endpoints.
This can help diagnose issues that might be related to how the frontend is making requests.

This test will:
1. Start the Django development server
2. Use curl to make POST requests to the endpoints
3. Analyze the responses to determine why 405 errors might be occurring
"""

import pytest
import subprocess
import json
import time
import os
import signal
import logging
from django.contrib.auth import get_user_model
from django.core.management import call_command
from threading import Thread

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()

@pytest.fixture(scope="module")
def django_server():
    """Start a Django development server for testing."""
    # Start the server in a separate thread
    def run_server():
        call_command('runserver', '8000', '--noreload')
    
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(3)
    
    yield
    
    # Cleanup (though with daemon=True, this may not be necessary)
    if server_thread.is_alive():
        os.kill(os.getpid(), signal.SIGINT)

@pytest.fixture
def admin_token():
    """Create an admin user and get a JWT token."""
    # Create admin user if it doesn't exist
    User = get_user_model()
    username = 'admin_curl_test'
    password = 'adminpassword'
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email='admin_curl@example.com',
            password=password,
            role='admin'
        )
    
    # Get token using curl
    cmd = [
        'curl', '-s', '-X', 'POST',
        'http://localhost:8000/api/users/token/',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"username": username, "password": password})
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    response = json.loads(result.stdout)
    
    return response.get('access', '')

@pytest.mark.django_db
class TestBrokerPostCurl:
    """Test class for broker POST endpoints using curl."""
    
    def test_post_branch_with_curl(self, django_server, admin_token):
        """Test POST request to /api/brokers/branches/ endpoint using curl."""
        # Skip if no token
        if not admin_token:
            pytest.skip("Could not get admin token")
        
        # Prepare branch data
        branch_data = {
            "name": "Curl Test Branch",
            "address": "123 Curl St",
            "phone": "5551234567",
            "email": "curlbranch@example.com"
        }
        
        # Test POST request with curl
        cmd = [
            'curl', '-s', '-X', 'POST',
            'http://localhost:8000/api/brokers/branches/',
            '-H', f'Authorization: Bearer {admin_token}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(branch_data)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl POST to /api/brokers/branches/ returned: {result.stdout}")
        
        # Check if we got a 405 error
        if "405" in result.stdout:
            logger.error("Received 405 Method Not Allowed from curl request")
            
            # Try with different content types
            content_types = [
                'application/json',
                'application/x-www-form-urlencoded',
                'multipart/form-data'
            ]
            
            for content_type in content_types:
                logger.info(f"Trying with Content-Type: {content_type}")
                if content_type == 'application/json':
                    cmd = [
                        'curl', '-s', '-X', 'POST',
                        'http://localhost:8000/api/brokers/branches/',
                        '-H', f'Authorization: Bearer {admin_token}',
                        '-H', f'Content-Type: {content_type}',
                        '-d', json.dumps(branch_data)
                    ]
                else:
                    # Convert to form data format
                    form_data = '&'.join([f"{k}={v}" for k, v in branch_data.items()])
                    cmd = [
                        'curl', '-s', '-X', 'POST',
                        'http://localhost:8000/api/brokers/branches/',
                        '-H', f'Authorization: Bearer {admin_token}',
                        '-H', f'Content-Type: {content_type}',
                        '-d', form_data
                    ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                logger.info(f"Curl POST with {content_type} returned: {result.stdout}")
            
            # Try without trailing slash
            cmd = [
                'curl', '-s', '-X', 'POST',
                'http://localhost:8000/api/brokers/branches',
                '-H', f'Authorization: Bearer {admin_token}',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(branch_data)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            logger.info(f"Curl POST without trailing slash returned: {result.stdout}")
        
        # Try GET request to see if the endpoint exists
        cmd = [
            'curl', '-s', '-X', 'GET',
            'http://localhost:8000/api/brokers/branches/',
            '-H', f'Authorization: Bearer {admin_token}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl GET to /api/brokers/branches/ returned status: {'200 OK' if result.stdout else 'Error'}")
        
        # Try OPTIONS request to see allowed methods
        cmd = [
            'curl', '-s', '-X', 'OPTIONS',
            'http://localhost:8000/api/brokers/branches/',
            '-H', f'Authorization: Bearer {admin_token}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl OPTIONS to /api/brokers/branches/ returned: {result.stdout}")
    
    def test_post_bdm_with_curl(self, django_server, admin_token):
        """Test POST request to /api/brokers/bdms/ endpoint using curl."""
        # Skip if no token
        if not admin_token:
            pytest.skip("Could not get admin token")
        
        # First create a branch to reference
        branch_data = {
            "name": "Curl Test Branch for BDM",
            "address": "456 Curl St",
            "phone": "5559876543",
            "email": "curlbdmbranch@example.com"
        }
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            'http://localhost:8000/api/brokers/branches/',
            '-H', f'Authorization: Bearer {admin_token}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(branch_data)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            branch_response = json.loads(result.stdout)
            branch_id = branch_response.get('id')
        except (json.JSONDecodeError, KeyError):
            logger.error(f"Could not create branch: {result.stdout}")
            branch_id = None
        
        # Prepare BDM data
        bdm_data = {
            "name": "Curl Test BDM",
            "email": "curlbdm@example.com",
            "phone": "5557654321"
        }
        
        if branch_id:
            bdm_data["branch_id"] = branch_id
        
        # Test POST request with curl
        cmd = [
            'curl', '-s', '-X', 'POST',
            'http://localhost:8000/api/brokers/bdms/',
            '-H', f'Authorization: Bearer {admin_token}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(bdm_data)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl POST to /api/brokers/bdms/ returned: {result.stdout}")
        
        # Check if we got a 405 error
        if "405" in result.stdout:
            logger.error("Received 405 Method Not Allowed from curl request")
            
            # Try with different content types
            content_types = [
                'application/json',
                'application/x-www-form-urlencoded',
                'multipart/form-data'
            ]
            
            for content_type in content_types:
                logger.info(f"Trying with Content-Type: {content_type}")
                if content_type == 'application/json':
                    cmd = [
                        'curl', '-s', '-X', 'POST',
                        'http://localhost:8000/api/brokers/bdms/',
                        '-H', f'Authorization: Bearer {admin_token}',
                        '-H', f'Content-Type: {content_type}',
                        '-d', json.dumps(bdm_data)
                    ]
                else:
                    # Convert to form data format
                    form_data = '&'.join([f"{k}={v}" for k, v in bdm_data.items()])
                    cmd = [
                        'curl', '-s', '-X', 'POST',
                        'http://localhost:8000/api/brokers/bdms/',
                        '-H', f'Authorization: Bearer {admin_token}',
                        '-H', f'Content-Type: {content_type}',
                        '-d', form_data
                    ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                logger.info(f"Curl POST with {content_type} returned: {result.stdout}")
            
            # Try without trailing slash
            cmd = [
                'curl', '-s', '-X', 'POST',
                'http://localhost:8000/api/brokers/bdms',
                '-H', f'Authorization: Bearer {admin_token}',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(bdm_data)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            logger.info(f"Curl POST without trailing slash returned: {result.stdout}")
            
            # Try the special create_with_branch endpoint
            special_data = bdm_data.copy()
            special_data.pop('branch_id', None)
            special_data.update({
                "branch_name": "New Branch for Curl BDM",
                "address": "789 Curl BDM Branch St",
                "branch_phone": "5551112222",
                "branch_email": "curlbdmbranch@example.com"
            })
            
            cmd = [
                'curl', '-s', '-X', 'POST',
                'http://localhost:8000/api/brokers/bdms/create_with_branch/',
                '-H', f'Authorization: Bearer {admin_token}',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(special_data)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            logger.info(f"Curl POST to create_with_branch endpoint returned: {result.stdout}")
        
        # Try GET request to see if the endpoint exists
        cmd = [
            'curl', '-s', '-X', 'GET',
            'http://localhost:8000/api/brokers/bdms/',
            '-H', f'Authorization: Bearer {admin_token}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl GET to /api/brokers/bdms/ returned status: {'200 OK' if result.stdout else 'Error'}")
        
        # Try OPTIONS request to see allowed methods
        cmd = [
            'curl', '-s', '-X', 'OPTIONS',
            'http://localhost:8000/api/brokers/bdms/',
            '-H', f'Authorization: Bearer {admin_token}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Curl OPTIONS to /api/brokers/bdms/ returned: {result.stdout}")
