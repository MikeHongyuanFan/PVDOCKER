# Frontend Error Tests

This directory contains tests to investigate and diagnose 404 errors reported by the frontend team.

## Reported Issues

The frontend team is receiving 404 errors for the following endpoints:

- `/api/borrowers/guarantors/` (GET)
- `/api/brokers/bdms/` (GET)
- `/api/brokers/branches/` (GET)

## Test Files

1. `test_frontend_404_errors.py` - General tests for all reported endpoints
2. `test_guarantor_endpoint.py` - Specific tests for the guarantors endpoint
3. `test_broker_endpoints.py` - Specific tests for the broker-related endpoints

## Running the Tests

To run these tests, use the following command from the project root:

```bash
cd backenddjango
python manage.py test tests.integration.frontenderrortests
```

Or using pytest:

```bash
cd backenddjango
pytest tests/integration/frontenderrortests
```

## Test Strategy

These tests use a comprehensive approach to diagnose the issues:

1. **URL Resolution Testing**: Check if Django's URL resolver can resolve the problematic URLs
2. **URL Reverse Testing**: Check if the URL names can be reversed to generate the correct URLs
3. **Endpoint Access Testing**: Test if the endpoints can be accessed with admin credentials
4. **Model Verification**: Verify that the required models exist
5. **Data Creation Testing**: Test creating data through the API to see if the endpoints work
6. **URL Variation Testing**: Test different URL variations to find working alternatives
7. **URL Pattern Inspection**: Inspect all URL patterns in the project to help diagnose issues
8. **API Root Testing**: Check the API root to see what endpoints are available

## Expected Outcomes

The tests will provide detailed logs that can help identify why the endpoints are returning 404 errors. Possible issues include:

- Missing URL patterns
- Incorrect URL naming
- Missing viewsets
- Incorrect router configuration
- App configuration issues

## Next Steps

After running the tests, review the logs to identify the root cause of the 404 errors. Based on the findings, you may need to:

1. Add missing URL patterns
2. Fix incorrect URL naming
3. Create missing viewsets
4. Update router configuration
5. Fix app configuration issues
