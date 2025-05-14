"""
Specific test for the guarantors endpoint to diagnose why it's returning 404.
This test will:
1. Check if the guarantors model exists
2. Create test data for guarantors
3. Test the endpoint with different URL variations
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
class TestGuarantorEndpoint:
    """Test class specifically for the guarantors endpoint."""
    
    def test_guarantor_model_exists(self):
        """Check if the Guarantor model exists."""
        try:
            Guarantor = apps.get_model('borrowers', 'Guarantor')
            logger.info(f"Guarantor model exists: {Guarantor}")
            assert Guarantor is not None, "Guarantor model does not exist"
        except LookupError:
            logger.error("Guarantor model does not exist")
            pytest.fail("Guarantor model does not exist")
    
    def test_create_guarantor(self, admin_client):
        """Test creating a guarantor through the API."""
        # First, create a borrower since guarantors are usually associated with borrowers
        borrower_data = {
            "first_name": "Test",
            "last_name": "Borrower",
            "email": "test.borrower@example.com",
            "phone": "1234567890",
            "address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "employment_type": "FULL_TIME",
            "employer_name": "Test Employer",
            "job_title": "Tester",
            "annual_income": 100000.00,
            "years_at_employer": 5
        }
        
        borrower_response = admin_client.post('/api/borrowers/', borrower_data, format='json')
        logger.info(f"Borrower creation response: {borrower_response.status_code}")
        logger.info(f"Borrower creation content: {borrower_response.content.decode('utf-8')}")
        
        if borrower_response.status_code == status.HTTP_201_CREATED:
            borrower_id = borrower_response.json()['id']
            
            # Now create a guarantor
            guarantor_data = {
                "borrower": borrower_id,
                "first_name": "Test",
                "last_name": "Guarantor",
                "email": "test.guarantor@example.com",
                "phone": "0987654321",
                "address": "456 Test St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "54321",
                "employment_type": "FULL_TIME",
                "employer_name": "Test Employer",
                "job_title": "Guarantor",
                "annual_income": 80000.00,
                "years_at_employer": 3,
                "relationship_to_borrower": "FAMILY"
            }
            
            guarantor_response = admin_client.post('/api/borrowers/guarantors/', guarantor_data, format='json')
            logger.info(f"Guarantor creation response: {guarantor_response.status_code}")
            logger.info(f"Guarantor creation content: {guarantor_response.content.decode('utf-8')}")
            
            # Try alternative URL if the first one fails
            if guarantor_response.status_code == status.HTTP_404_NOT_FOUND:
                alternative_urls = [
                    '/api/guarantors/',
                    f'/api/borrowers/{borrower_id}/guarantors/',
                    '/api/borrowers/guarantor/'
                ]
                
                for url in alternative_urls:
                    alt_response = admin_client.post(url, guarantor_data, format='json')
                    logger.info(f"Alternative URL {url} response: {alt_response.status_code}")
                    if alt_response.status_code != status.HTTP_404_NOT_FOUND:
                        logger.info(f"Found working URL: {url}")
                        break
        else:
            logger.error("Failed to create borrower, skipping guarantor creation")
    
    def test_guarantor_urls(self, admin_client):
        """Test different URL variations for guarantors."""
        url_variations = [
            '/api/borrowers/guarantors/',
            '/api/guarantors/',
            '/api/borrowers/guarantor/',
            '/api/borrowers/guarantors',  # Without trailing slash
        ]
        
        for url in url_variations:
            response = admin_client.get(url)
            logger.info(f"URL: {url}, Status: {response.status_code}")
            if response.status_code == status.HTTP_200_OK:
                logger.info(f"Found working URL: {url}")
                logger.info(f"Response: {response.content.decode('utf-8')[:200]}...")
    
    def test_borrowers_app_urls(self):
        """Inspect the borrowers app URLs to find the guarantors endpoint."""
        from borrowers.urls import urlpatterns
        
        logger.info("Borrowers app URL patterns:")
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern'):
                logger.info(f"Pattern: {pattern.pattern}")
            if hasattr(pattern, 'name'):
                logger.info(f"Name: {pattern.name}")
            if hasattr(pattern, 'callback'):
                logger.info(f"Callback: {pattern.callback.__name__ if hasattr(pattern.callback, '__name__') else str(pattern.callback)}")
            logger.info("---")
        
        # Check if there's a router that might include guarantors
        from borrowers.urls import router
        logger.info(f"Router registry: {router.registry}")
        
        # Check if there's a guarantor viewset
        try:
            from borrowers.views import GuarantorViewSet
            logger.info(f"GuarantorViewSet exists: {GuarantorViewSet}")
        except ImportError:
            logger.error("GuarantorViewSet does not exist")
            
            # Check all views in the borrowers app
            import inspect
            from borrowers import views
            
            for name, obj in inspect.getmembers(views):
                if inspect.isclass(obj) and 'Guarantor' in name:
                    logger.info(f"Found potential guarantor view: {name}")
                    
    def test_api_root(self, admin_client):
        """Test the API root to see what endpoints are available."""
        response = admin_client.get('/api/')
        logger.info(f"API root response: {response.status_code}")
        if response.status_code == status.HTTP_200_OK:
            logger.info(f"API root content: {response.content.decode('utf-8')}")
            
            # Check if guarantors is listed in the API root
            content = response.content.decode('utf-8')
            if 'guarantor' in content.lower():
                logger.info("Guarantors endpoint is listed in the API root")
            else:
                logger.info("Guarantors endpoint is NOT listed in the API root")
