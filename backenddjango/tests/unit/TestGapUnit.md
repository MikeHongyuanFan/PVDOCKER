# Unit Test Coverage Gap Analysis

## Overview

This document identifies the gaps in our unit test coverage and outlines a phased plan to address them. Based on our current coverage report, we have an overall unit test coverage of 57%, with significant variations across different components.

## Current Coverage Summary

| Component Type | Coverage Range | Assessment |
|---------------|---------------|------------|
| Models | 97-100% | Excellent |
| Serializers | 54-100% | Good to Excellent |
| Views | 38-93% | Poor to Excellent |
| Services | 0-43% | Poor |
| Filters | 0-97% | Poor to Excellent |
| Tasks | 0% | Missing |
| WebSocket Consumers | 0% | Missing |

## Detailed Gap Analysis

### Critical Gaps (0-30% Coverage)

1. **Background Tasks (0%)**
   - All Celery tasks in `applications/tasks.py`
   - Email notification tasks
   - Document generation tasks
   - Scheduled report generation

2. **WebSocket Consumers (0%)**
   - Real-time notification system in `users/consumers.py`
   - WebSocket connection handling
   - Authentication via WebSockets
   - Message broadcasting

3. **Services with Low Coverage**
   - `applications/services.py` (14%)
   - `borrowers/services.py` (0%)
   - `documents/services.py` (0%)

### Moderate Gaps (30-70% Coverage)

1. **Serializers with Moderate Coverage**
   - `applications/serializers.py` (54%)
   - `documents/serializers.py` (68%)

2. **Views with Moderate Coverage**
   - `applications/views.py` (38%)
   - `brokers/views.py` (43%)

### Minor Gaps (70-90% Coverage)

1. **Filters**
   - `brokers/filters.py` (85%)
   - `borrowers/filters.py` (77%)

2. **Views with Good Coverage**
   - `borrowers/views.py` (80%)
   - `reports/views.py` (89%)

## Implementation Plan

### Phase 1: Fix Existing Tests & Critical Infrastructure (Weeks 1-2)

**Objectives:**
- Fix failing unit tests
- Set up proper test infrastructure
- Address pytest dependency issues

**Tasks:**
1. Install pytest and required dependencies
   ```bash
   docker exec -it lianv3-501a294797023b7f3fa802ddb963f1a4b1577785-backend-1 pip install pytest pytest-django
   ```

2. Fix model test failures
   - Update Borrower model tests to match actual model fields
   - Fix string representation tests for User, Broker, and Notification models

3. Create proper test fixtures and utilities
   - Set up pytest fixtures for common test objects
   - Create mock utilities for external dependencies

### Phase 2: Critical Gaps - Services & Tasks (Weeks 3-4)

**Objectives:**
- Increase service coverage from <20% to >60%
- Add initial task testing infrastructure

**Tasks:**
1. Application Services Testing
   - Test application creation and validation services
   - Test status transition services
   - Test fee calculation services

2. Document Services Testing
   - Test document generation services
   - Test document validation services
   - Test document storage services

3. Borrower Services Testing
   - Test borrower validation services
   - Test credit check services
   - Test borrower relationship services

4. Initial Task Testing
   - Set up Celery test infrastructure
   - Test basic task execution
   - Test task scheduling

### Phase 3: WebSocket & Advanced Features (Weeks 5-6)

**Objectives:**
- Implement WebSocket testing
- Test advanced features and edge cases

**Tasks:**
1. WebSocket Consumer Testing
   - Test WebSocket connection handling
   - Test authentication via WebSockets
   - Test message broadcasting
   - Test real-time notification delivery

2. Advanced Task Testing
   - Test task chaining
   - Test error handling in tasks
   - Test periodic tasks

3. Edge Case Testing
   - Test service behavior with invalid inputs
   - Test error handling in services
   - Test transaction rollback scenarios

### Phase 4: Moderate Gaps - Views & Serializers (Weeks 7-8)

**Objectives:**
- Increase view coverage from 38-93% to >80% across all apps
- Increase serializer coverage to >90% across all apps

**Tasks:**
1. View Testing
   - Test permission handling
   - Test filtering and pagination
   - Test error responses
   - Test custom actions

2. Serializer Testing
   - Test validation logic
   - Test custom field handling
   - Test nested serializer behavior
   - Test serializer methods

### Phase 5: Comprehensive Testing & Optimization (Weeks 9-10)

**Objectives:**
- Achieve >80% overall unit test coverage
- Optimize test performance
- Ensure test maintainability

**Tasks:**
1. Fill Remaining Gaps
   - Address any remaining low-coverage areas
   - Add tests for helper functions and utilities
   - Test configuration and settings

2. Test Optimization
   - Reduce test execution time
   - Implement parallel test execution
   - Optimize test fixtures

3. Documentation & Maintenance
   - Document test patterns and best practices
   - Set up test coverage reporting in CI
   - Create test maintenance guidelines

## Test Implementation Priorities

### Priority 1: High Impact, Low Coverage
- Application services (14% coverage)
- Document services (0% coverage)
- Background tasks (0% coverage)

### Priority 2: Core Functionality
- WebSocket consumers (0% coverage)
- Application views (38% coverage)
- User services (43% coverage)

### Priority 3: Supporting Components
- Serializers with <70% coverage
- Filters with <80% coverage
- Permission classes with <60% coverage

## Success Metrics

- **Short-term:** Increase overall unit test coverage to 70% by the end of Phase 3
- **Medium-term:** Achieve >80% coverage across all critical components by the end of Phase 5
- **Long-term:** Maintain >85% overall coverage and ensure all new code has >90% coverage

## Resources Required

- Developer time: Approximately 160 hours (4 weeks full-time equivalent)
- Additional dependencies: pytest, pytest-django, pytest-cov, factory-boy, pytest-celery
- CI integration: Coverage reporting in build pipeline

## Conclusion

This phased approach will systematically address the gaps in our unit test coverage, starting with the most critical areas and working toward comprehensive coverage. By following this plan, we can significantly improve the reliability and maintainability of our codebase while reducing the risk of regressions during future development.
## Skipped API Tests
 
The following API tests are currently being skipped due to missing or changed endpoints. These represent gaps in our API implementation or test coverage that need to be addressed:

### Application Views
1. ~~**test_update_application_stage** - Endpoint: `/api/applications/{id}/stage/`~~ ✅ FIXED
 - Purpose: Update the stage of an application
 - Expected functionality: PUT request to change application stage with notes
 - Current status: Implemented and tested successfully

2. ~~**test_update_application_borrowers** - Endpoint: `/api/applications/{id}/borrowers/`~~ ✅ FIXED
 - Purpose: Associate borrowers with an application
 - Expected functionality: PUT request to update borrower associations
 - Current status: Implemented and tested successfully

3. ~~**test_sign_application** - Endpoint: `/api/applications/{id}/sign/`~~ ✅ FIXED
 - Purpose: Add electronic signature to an application
 - Expected functionality: POST request with signature data and name
 - Current status: Implemented and tested successfully

4. ~~**test_filter_applications_by_stage** - Endpoint: `/api/applications/?stage=inquiry`~~ ✅ FIXED
 - Purpose: Filter applications by their stage
 - Expected functionality: GET request with stage filter parameter
 - Current status: Implemented and tested successfully

### Document Views
1. ~~**test_update_document** - Endpoint: `/api/documents/{id}/`~~ ✅ FIXED
 - Purpose: Update document metadata
 - Expected functionality: PATCH request to update document title, description, etc.
 - Current status: Implemented and tested successfully

2. ~~**test_update_document_with_file** - Endpoint: `/api/documents/{id}/`~~ ✅ FIXED
 - Purpose: Update document with a new file version
 - Expected functionality: PATCH request with file creates a new version
 - Current status: Implemented and tested successfully

### Document Views
1. **test_update_document** - Endpoint: `/api/documents/{id}/`
 - Purpose: Update document metadata
 - Expected functionality: PATCH request to update document title and type
 - Current status: Validation error (400) - may require additional fields

2. **test_filter_documents_by_type** - Endpoint: `/api/documents/?document_type=contract`
 - Purpose: Filter documents by their type
 - Expected functionality: GET request with document_type filter parameter
 - Current status: Filter parameter may not be supported (400)

3. **test_mark_fee_as_paid** - Endpoint: `/api/fees/{id}/mark-paid/`
 - Purpose: Mark a fee as paid
 - Expected functionality: POST request to update fee status
 - Current status: Endpoint may not return expected response format

 ### Borrower Views
1. **test_list_guarantors** - Endpoint: `/api/guarantors/`
 - Purpose: List all guarantors
 - Expected functionality: GET request to retrieve guarantors
 - Current status: Endpoint may not exist

2. **test_create_guarantor** - Endpoint: `/api/guarantors/`
 - Purpose: Create a new guarantor
 - Expected functionality: POST request to create guarantor
 - Current status: Endpoint may not exist

3. **test_filter_guarantors_by_application** - Endpoint: `/api/guarantors/?application={id}`
 - Purpose: Filter guarantors by application
 - Expected functionality: GET request with application filter parameter
 - Current status: Endpoint may not exist

### WebSocket Consumers
All WebSocket consumer tests are failing due to authentication issues:

1. **test_connect_authenticated** - WebSocket connection with authenticated user
2. **test_connect_unauthenticated** - WebSocket connection with unauthenticated user
3. **test_receive_get_unread_count** - WebSocket message to get unread notification count
4. **test_notification_message** - WebSocket notification message handling
5. **test_notification_count_update** - WebSocket notification count update
6. **test_disconnect** - WebSocket disconnection handling

The WebSocket tests are failing with a `KeyError: 'user'` error, indicating that the authentication middleware is not properly adding the user to the WebSocket scope.

## Next Steps for API Test Gaps

1. **Implement Missing Endpoints**: Create the missing API endpoints for application stage updates, borrower associations, and document operations.

2. **Fix WebSocket Authentication**: Update the WebSocket authentication middleware to properly add the user to the scope.

3. **Update API Documentation**: Ensure that all API endpoints are properly documented in the Swagger/OpenAPI documentation.

4. **Standardize API Response Formats**: Ensure consistent response formats across all API endpoints.

5. **Add Integration Tests**: Create integration tests that verify the end-to-end functionality of these endpoints.
