"""
Specific test for the broker-related endpoints to diagnose why they're returning 404.
This test will:
1. Check if the BDM and Branch models exist
2. Create test data for brokers, BDMs, and branches
3. Test the endpoints with different URL variations
4. Provide detailed diagnostics
"""

import pytest
import logging
from django.urls import reverse, resolve, NoReverseMatch
from rest_framework import status
from django.apps import apps

# Set up logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
class TestBrokerEndpoints:
    """Test class specifically for the broker-related endpoints."""
    
    def test_broker_models_exist(self):
        """Check if the Broker, BDM, and Branch models exist."""
        try:
            Broker = apps.get_model('brokers', 'Broker')
            logger.info(f"Broker model exists: {Broker}")
            assert Broker is not None, "Broker model does not exist"
        except LookupError:
            logger.error("Broker model does not exist")
            pytest.fail("Broker model does not exist")
            
        try:
            BDM = apps.get_model('brokers', 'BDM')
            logger.info(f"BDM model exists: {BDM}")
            assert BDM is not None, "BDM model does not exist"
        except LookupError:
            logger.error("BDM model does not exist")
            pytest.fail("BDM model does not exist")
            
        try:
            Branch = apps.get_model('brokers', 'Branch')
            logger.info(f"Branch model exists: {Branch}")
            assert Branch is not None, "Branch model does not exist"
        except LookupError:
            logger.error("Branch model does not exist")
            pytest.fail("Branch model does not exist")
    
    def test_create_broker(self, admin_client):
        """Test creating a broker through the API."""
        broker_data = {
            "name": "Test Broker",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_phone": "1234567890",
            "address": "123 Broker St",
            "city": "Broker City",
            "state": "BC",
            "zip_code": "12345",
            "status": "ACTIVE"
        }
        
        broker_response = admin_client.post('/api/brokers/', broker_data, format='json')
        logger.info(f"Broker creation response: {broker_response.status_code}")
        logger.info(f"Broker creation content: {broker_response.content.decode('utf-8')}")
        
        if broker_response.status_code == status.HTTP_201_CREATED:
            broker_id = broker_response.json()['id']
            return broker_id
        else:
            logger.error("Failed to create broker")
            return None
    
    def test_create_bdm(self, admin_client):
        """Test creating a BDM through the API."""
        broker_id = self.test_create_broker(admin_client)
        if not broker_id:
            pytest.skip("Broker creation failed, skipping BDM creation")
            
        bdm_data = {
            "broker": broker_id,
            "name": "Test BDM",
            "email": "bdm@example.com",
            "phone": "0987654321",
            "status": "ACTIVE"
        }
        
        bdm_response = admin_client.post('/api/brokers/bdms/', bdm_data, format='json')
        logger.info(f"BDM creation response: {bdm_response.status_code}")
        logger.info(f"BDM creation content: {bdm_response.content.decode('utf-8')}")
        
        # Try alternative URL if the first one fails
        if bdm_response.status_code == status.HTTP_404_NOT_FOUND:
            alternative_urls = [
                '/api/bdms/',
                f'/api/brokers/{broker_id}/bdms/',
                '/api/brokers/bdm/'
            ]
            
            for url in alternative_urls:
                alt_response = admin_client.post(url, bdm_data, format='json')
                logger.info(f"Alternative URL {url} response: {alt_response.status_code}")
                if alt_response.status_code != status.HTTP_404_NOT_FOUND:
                    logger.info(f"Found working URL: {url}")
                    break
    
    def test_create_branch(self, admin_client):
        """Test creating a branch through the API."""
        broker_id = self.test_create_broker(admin_client)
        if not broker_id:
            pytest.skip("Broker creation failed, skipping branch creation")
            
        branch_data = {
            "broker": broker_id,
            "name": "Test Branch",
            "address": "456 Branch St",
            "city": "Branch City",
            "state": "BC",
            "zip_code": "54321",
            "status": "ACTIVE"
        }
        
        branch_response = admin_client.post('/api/brokers/branches/', branch_data, format='json')
        logger.info(f"Branch creation response: {branch_response.status_code}")
        logger.info(f"Branch creation content: {branch_response.content.decode('utf-8')}")
        
        # Try alternative URL if the first one fails
        if branch_response.status_code == status.HTTP_404_NOT_FOUND:
            alternative_urls = [
                '/api/branches/',
                f'/api/brokers/{broker_id}/branches/',
                '/api/brokers/branch/'
            ]
            
            for url in alternative_urls:
                alt_response = admin_client.post(url, branch_data, format='json')
                logger.info(f"Alternative URL {url} response: {alt_response.status_code}")
                if alt_response.status_code != status.HTTP_404_NOT_FOUND:
                    logger.info(f"Found working URL: {url}")
                    break
    
    def test_broker_urls(self, admin_client):
        """Test different URL variations for broker-related endpoints."""
        url_variations = [
            # BDM URLs
            '/api/brokers/bdms/',
            '/api/bdms/',
            '/api/brokers/bdm/',
            '/api/brokers/bdms',  # Without trailing slash
            
            # Branch URLs
            '/api/brokers/branches/',
            '/api/branches/',
            '/api/brokers/branch/',
            '/api/brokers/branches',  # Without trailing slash
            
            # Base broker URL
            '/api/brokers/'
        ]
        
        for url in url_variations:
            response = admin_client.get(url)
            logger.info(f"URL: {url}, Status: {response.status_code}")
            if response.status_code == status.HTTP_200_OK:
                logger.info(f"Found working URL: {url}")
                logger.info(f"Response: {response.content.decode('utf-8')[:200]}...")
    
    def test_brokers_app_urls(self):
        """Inspect the brokers app URLs to find the BDM and Branch endpoints."""
        from brokers.urls import urlpatterns, router
        
        logger.info("Brokers app URL patterns:")
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern'):
                logger.info(f"Pattern: {pattern.pattern}")
            if hasattr(pattern, 'name'):
                logger.info(f"Name: {pattern.name}")
            if hasattr(pattern, 'callback'):
                logger.info(f"Callback: {pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)}")
            logger.info("---")
        
        # Check the router registry
        logger.info(f"Router registry: {router.registry}")
        
        # Check if there are BDM and Branch viewsets
        try:
            from brokers.views import BDMViewSet, BranchViewSet
            logger.info(f"BDMViewSet exists: {BDMViewSet}")
            logger.info(f"BranchViewSet exists: {BranchViewSet}")
        except ImportError as e:
            logger.error(f"Error importing viewsets: {e}")
            
            # Check all views in the brokers app
            import inspect
            from brokers import views
            
            for name, obj in inspect.getmembers(views):
                if inspect.isclass(obj) and ('BDM' in name or 'Branch' in name):
                    logger.info(f"Found potential viewset: {name}")
                    
    def test_api_root(self, admin_client):
        """Test the API root to see what endpoints are available."""
        response = admin_client.get('/api/')
        logger.info(f"API root response: {response.status_code}")
        if response.status_code == status.HTTP_200_OK:
            logger.info(f"API root content: {response.content.decode('utf-8')}")
            
            # Check if bdms and branches are listed in the API root
            content = response.content.decode('utf-8')
            if 'bdm' in content.lower():
                logger.info("BDMs endpoint is listed in the API root")
            else:
                logger.info("BDMs endpoint is NOT listed in the API root")
                
            if 'branch' in content.lower():
                logger.info("Branches endpoint is listed in the API root")
            else:
                logger.info("Branches endpoint is NOT listed in the API root")
