"""
Test script that inspects the ViewSet configurations to diagnose why POST requests
might be returning 405 Method Not Allowed errors.

This test will:
1. Inspect the ViewSet classes to check if POST is allowed
2. Check the router configuration
3. Examine the permission classes
4. Test the serializers
"""

import pytest
import inspect
import logging
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import resolve, reverse

# Set up logging
logger = logging.getLogger(__name__)

@pytest.mark.django_db
class TestBrokerViewSetInspection:
    """Test class for inspecting broker ViewSets."""
    
    def test_branch_viewset_inspection(self):
        """Inspect the BranchViewSet to check if POST is allowed."""
        try:
            from brokers.views import BranchViewSet
            
            # Check if BranchViewSet is a ModelViewSet (which should allow POST)
            logger.info(f"BranchViewSet is a ModelViewSet: {issubclass(BranchViewSet, viewsets.ModelViewSet)}")
            
            # Check http_method_names
            http_method_names = getattr(BranchViewSet, 'http_method_names', [])
            logger.info(f"BranchViewSet http_method_names: {http_method_names}")
            logger.info(f"POST in http_method_names: {'post' in http_method_names}")
            
            # Check if create method is overridden
            has_create = hasattr(BranchViewSet, 'create')
            logger.info(f"BranchViewSet has create method: {has_create}")
            
            if has_create:
                # Check if create method is calling super().create()
                create_source = inspect.getsource(BranchViewSet.create)
                logger.info(f"BranchViewSet create method source: {create_source}")
            
            # Check permission classes
            get_permissions = getattr(BranchViewSet, 'get_permissions', None)
            if get_permissions:
                logger.info(f"BranchViewSet has get_permissions method")
                # Try to determine permissions for create action
                try:
                    instance = BranchViewSet()
                    instance.action = 'create'
                    permissions = instance.get_permissions()
                    logger.info(f"Permissions for create action: {permissions}")
                except Exception as e:
                    logger.error(f"Error getting permissions: {e}")
            
            # Check serializer class
            serializer_class = getattr(BranchViewSet, 'serializer_class', None)
            logger.info(f"BranchViewSet serializer_class: {serializer_class}")
            
            # Check if there's a get_serializer_class method
            get_serializer_class = getattr(BranchViewSet, 'get_serializer_class', None)
            if get_serializer_class:
                logger.info(f"BranchViewSet has get_serializer_class method")
                try:
                    instance = BranchViewSet()
                    instance.action = 'create'
                    serializer_class = instance.get_serializer_class()
                    logger.info(f"Serializer class for create action: {serializer_class}")
                except Exception as e:
                    logger.error(f"Error getting serializer class: {e}")
            
        except ImportError:
            logger.error("Could not import BranchViewSet")
    
    def test_bdm_viewset_inspection(self):
        """Inspect the BDMViewSet to check if POST is allowed."""
        try:
            from brokers.views import BDMViewSet
            
            # Check if BDMViewSet is a ModelViewSet (which should allow POST)
            logger.info(f"BDMViewSet is a ModelViewSet: {issubclass(BDMViewSet, viewsets.ModelViewSet)}")
            
            # Check http_method_names
            http_method_names = getattr(BDMViewSet, 'http_method_names', [])
            logger.info(f"BDMViewSet http_method_names: {http_method_names}")
            logger.info(f"POST in http_method_names: {'post' in http_method_names}")
            
            # Check if create method is overridden
            has_create = hasattr(BDMViewSet, 'create')
            logger.info(f"BDMViewSet has create method: {has_create}")
            
            if has_create:
                # Check if create method is calling super().create()
                create_source = inspect.getsource(BDMViewSet.create)
                logger.info(f"BDMViewSet create method source: {create_source}")
            
            # Check permission classes
            get_permissions = getattr(BDMViewSet, 'get_permissions', None)
            if get_permissions:
                logger.info(f"BDMViewSet has get_permissions method")
                # Try to determine permissions for create action
                try:
                    instance = BDMViewSet()
                    instance.action = 'create'
                    permissions = instance.get_permissions()
                    logger.info(f"Permissions for create action: {permissions}")
                except Exception as e:
                    logger.error(f"Error getting permissions: {e}")
            
            # Check serializer class
            serializer_class = getattr(BDMViewSet, 'serializer_class', None)
            logger.info(f"BDMViewSet serializer_class: {serializer_class}")
            
            # Check if there's a get_serializer_class method
            get_serializer_class = getattr(BDMViewSet, 'get_serializer_class', None)
            if get_serializer_class:
                logger.info(f"BDMViewSet has get_serializer_class method")
                try:
                    instance = BDMViewSet()
                    instance.action = 'create'
                    serializer_class = instance.get_serializer_class()
                    logger.info(f"Serializer class for create action: {serializer_class}")
                except Exception as e:
                    logger.error(f"Error getting serializer class: {e}")
            
            # Check special actions
            for name, method in inspect.getmembers(BDMViewSet, predicate=inspect.isfunction):
                if hasattr(method, 'mapping'):
                    logger.info(f"Found action method: {name} with mapping {method.mapping}")
                    if 'post' in method.mapping.values():
                        logger.info(f"Action {name} supports POST")
            
        except ImportError:
            logger.error("Could not import BDMViewSet")
    
    def test_router_configuration(self):
        """Inspect the router configuration to check if POST is properly routed."""
        try:
            from brokers.urls import router
            
            # Check router registry
            logger.info(f"Router registry: {router.registry}")
            
            # Check if branches and bdms are registered
            for prefix, viewset, basename in router.registry:
                logger.info(f"Registered route: prefix={prefix}, viewset={viewset}, basename={basename}")
                
                # Check if this viewset allows POST
                http_method_names = getattr(viewset, 'http_method_names', [])
                logger.info(f"ViewSet {viewset.__name__} http_method_names: {http_method_names}")
                logger.info(f"POST in http_method_names: {'post' in http_method_names}")
            
            # Check generated URLs
            urls = router.urls
            for url in urls:
                logger.info(f"URL pattern: {url.pattern}")
                if hasattr(url, 'name'):
                    logger.info(f"URL name: {url.name}")
                if hasattr(url, 'callback'):
                    logger.info(f"URL callback: {url.callback}")
                    # Check if this callback allows POST
                    if hasattr(url.callback, 'actions'):
                        logger.info(f"Callback actions: {url.callback.actions}")
                        logger.info(f"POST in actions: {'post' in url.callback.actions}")
                logger.info("---")
            
        except ImportError:
            logger.error("Could not import router from brokers.urls")
    
    def test_url_resolution(self):
        """Test URL resolution to check if the correct view is being used."""
        try:
            # Try to resolve the URLs
            branch_url = '/api/brokers/branches/'
            bdm_url = '/api/brokers/bdms/'
            
            try:
                branch_resolver = resolve(branch_url)
                logger.info(f"Branch URL resolves to: {branch_resolver.func}")
                logger.info(f"Branch URL kwargs: {branch_resolver.kwargs}")
                logger.info(f"Branch URL args: {branch_resolver.args}")
                
                # Check if this view allows POST
                if hasattr(branch_resolver.func, 'actions'):
                    logger.info(f"Branch view actions: {branch_resolver.func.actions}")
                    logger.info(f"POST in actions: {'post' in branch_resolver.func.actions}")
            except Exception as e:
                logger.error(f"Error resolving branch URL: {e}")
            
            try:
                bdm_resolver = resolve(bdm_url)
                logger.info(f"BDM URL resolves to: {bdm_resolver.func}")
                logger.info(f"BDM URL kwargs: {bdm_resolver.kwargs}")
                logger.info(f"BDM URL args: {bdm_resolver.args}")
                
                # Check if this view allows POST
                if hasattr(bdm_resolver.func, 'actions'):
                    logger.info(f"BDM view actions: {bdm_resolver.func.actions}")
                    logger.info(f"POST in actions: {'post' in bdm_resolver.func.actions}")
            except Exception as e:
                logger.error(f"Error resolving BDM URL: {e}")
            
        except Exception as e:
            logger.error(f"Error in URL resolution test: {e}")
    
    def test_serializer_validation(self):
        """Test serializer validation to check if there are issues with the data."""
        try:
            from brokers.serializers import BranchSerializer, BDMSerializer
            
            # Test BranchSerializer
            branch_data = {
                "name": "Test Branch",
                "address": "123 Test St",
                "phone": "1234567890",
                "email": "branch@example.com"
            }
            
            branch_serializer = BranchSerializer(data=branch_data)
            is_valid = branch_serializer.is_valid()
            logger.info(f"BranchSerializer validation result: {is_valid}")
            if not is_valid:
                logger.error(f"BranchSerializer errors: {branch_serializer.errors}")
            
            # Test BDMSerializer
            bdm_data = {
                "name": "Test BDM",
                "email": "bdm@example.com",
                "phone": "0987654321",
                "branch_name": "New Branch",
                "address": "456 New Branch St",
                "branch_phone": "5551234567",
                "branch_email": "newbranch@example.com"
            }
            
            bdm_serializer = BDMSerializer(data=bdm_data)
            is_valid = bdm_serializer.is_valid()
            logger.info(f"BDMSerializer validation result: {is_valid}")
            if not is_valid:
                logger.error(f"BDMSerializer errors: {bdm_serializer.errors}")
            
        except ImportError:
            logger.error("Could not import serializers")
