# Broker Endpoints Testing

This directory contains test scripts specifically designed to diagnose the 405 Method Not Allowed errors reported by the frontend team when making POST requests to `/api/brokers/branches` and `/api/brokers/bdms` endpoints.

## Test Files

1. **test_broker_post_endpoints.py**
   - Tests POST requests to both endpoints using Django's test client
   - Tries different request formats and content types
   - Checks if the endpoints allow POST methods
   - Provides detailed error information

2. **test_broker_post_curl.py**
   - Uses subprocess to run curl commands against the endpoints
   - Simulates how the frontend might be making requests
   - Tests different content types and URL formats
   - Checks OPTIONS requests to see allowed methods

3. **test_broker_viewset_inspection.py**
   - Inspects the ViewSet classes to check if POST is allowed
   - Examines the router configuration
   - Checks permission classes
   - Tests serializer validation

## How to Run the Tests

Run the tests using pytest:

```bash
cd backenddjango
python -m pytest tests/integration/frontenderrortests/test_broker_post_endpoints.py -v
python -m pytest tests/integration/frontenderrortests/test_broker_viewset_inspection.py -v
python -m pytest tests/integration/frontenderrortests/test_broker_post_curl.py -v
```

## Common Causes of 405 Method Not Allowed

1. **ViewSet Configuration Issues**
   - The ViewSet might not be inheriting from ModelViewSet
   - The http_method_names list might be overridden and not include 'post'
   - The create method might be overridden incorrectly

2. **Router Configuration Issues**
   - The router might not be registering the ViewSet correctly
   - URL patterns might be conflicting

3. **Permission Issues**
   - The permission classes might be denying POST requests
   - The user might not have the required permissions

4. **Middleware Issues**
   - CSRF middleware might be blocking POST requests
   - Custom middleware might be interfering

5. **URL Configuration Issues**
   - The URL might be registered with a different pattern than expected
   - Trailing slashes might be required but missing

## Potential Fixes

1. **Check ViewSet Configuration**
   ```python
   class BranchViewSet(viewsets.ModelViewSet):
       # Make sure http_method_names includes 'post'
       http_method_names = ['get', 'post', 'put', 'patch', 'delete']
   ```

2. **Check Router Registration**
   ```python
   router = DefaultRouter()
   router.register(r'branches', views.BranchViewSet)
   router.register(r'bdms', views.BDMViewSet)
   ```

3. **Check Permissions**
   ```python
   def get_permissions(self):
       if self.action in ['create']:
           permission_classes = [IsAuthenticated, IsAdmin]
       else:
           permission_classes = [IsAuthenticated]
       return [permission() for permission in permission_classes]
   ```

4. **Check URL Trailing Slashes**
   - Django typically requires trailing slashes in URLs
   - Make sure the frontend is including the trailing slash in requests

5. **Check Content Type**
   - Make sure the frontend is sending the correct Content-Type header
   - For JSON data, use 'Content-Type: application/json'

## Next Steps

After running the tests, review the logs to identify the specific cause of the 405 errors. The most likely issues are:

1. Permission problems - check if the user has admin permissions
2. URL format issues - check if trailing slashes are being used correctly
3. Content type issues - check if the correct content type is being sent
4. ViewSet configuration - check if POST is allowed in the ViewSet
