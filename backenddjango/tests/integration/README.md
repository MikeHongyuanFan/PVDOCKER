# Integration Tests for CRM Loan Management System

This directory contains integration tests for the CRM Loan Management System. These tests focus on admin user functionality with 100% API access.

## Admin-Focused Testing Strategy

Our integration tests focus exclusively on admin users who have full access to all APIs. This approach offers several advantages:

1. **Comprehensive API Coverage**: Admin users can access all endpoints, allowing us to test the entire API surface.
2. **Simplified Authentication**: We only need to manage admin credentials for all tests.
3. **Full Data Access**: Admin users can view and manipulate all data, enabling thorough testing of data relationships.
4. **Workflow Testing**: We can test complete workflows from start to finish without permission barriers.

## Setup

### Database Configuration

Integration tests use a dedicated PostgreSQL database. To set up the database:

1. Create a PostgreSQL database named `crm_integration_test`:

```bash
createdb crm_integration_test
```

2. Configure database access in `settings_integration.py` if needed.

### Running Tests

To run the integration tests:

```bash
# Run all integration tests
python manage.py test tests.integration

# Run specific test file
python manage.py test tests.integration.test_db_reset

# Run with pytest (recommended)
pytest tests/integration/
```

## Test Structure

- `conftest.py`: Contains pytest fixtures and configuration
- `base.py`: Contains the `AdminIntegrationTestCase` base class
- `fixtures/`: Contains test data fixtures
- `test_*.py`: Test files organized by functionality

## Test Data

Test data is managed through:

1. Fixtures in JSON format in the `fixtures/` directory
2. Setup methods in test classes
3. API calls to create necessary data

## Best Practices

1. Each test should be independent and not rely on other tests
2. Use the base `AdminIntegrationTestCase` class for common functionality
3. Clean up resources after tests
4. Use descriptive test names that explain the scenario
5. Include clear assertion messages

## Troubleshooting

### Database Issues

If you encounter database issues:

1. Ensure PostgreSQL is running
2. Check database connection settings in `settings_integration.py`
3. Try recreating the test database:

```bash
dropdb crm_integration_test
createdb crm_integration_test
```

### Authentication Issues

If you encounter authentication issues:

1. Check that JWT tokens are being generated correctly
2. Verify that the admin user has the correct permissions
3. Check that the admin user is being created properly in the test setup
