# Sprint 1 Implementation Strategy

## Milestone 1: Critical Missing Components (Weeks 1-2)

### 1. DocuSign Integration
0. ** Connection detail: **
User ID 0500040d-c49a-453b-95dd-40302fd1bdca
   API accountID b23f1b1d-e370-43ec-a8e6-1533d837ec0a
Integration key:783bcc77-f364-4d22-800d-f988e9b2b20e	
secret key: ed6ed069-7ef8-469c-b3ba-2f2dbe2f0d13
Account base URL: https://demo.docusign.net
1. **Day 1-2: Setup & Authentication**
   - Create DocuSign developer account
   - Install `docusign-esign` Python package
   - Implement authentication service with OAuth flow
   - Create environment variables for DocuSign credentials

2. **Day 3-4: Core Integration**
   - Create `EnvelopeService` in `documents/services.py`
   - Implement document preparation and envelope creation
   - Add signature field placement logic

3. **Day 5: API Endpoint**
   - Create `POST /api/documents/{id}/send-for-signature/` endpoint
   - Implement serializers for request/response
   - Add permission checks

4. **Day 6-7: Testing & Documentation**
   - Write unit tests for DocuSign service
   - Create integration tests for the API endpoint
   - Document the API in Swagger

### 2. Email Send-As Functionality
1. **Day 8-9: Backend Service**
   - Extend email service to support send-as functionality
   - Create `SentEmailLog` model to track email history
   - Implement permission checks for send-as capability

2. **Day 10: API Endpoint**
   - Create `POST /api/emails/send/` endpoint
   - Implement request validation and security controls
   - Add tests for the endpoint

## Milestone 2: Calculator API Improvements (Week 3) Done

1. **Day 11-12: Model & Logic Updates**
   - Add new fields to calculator model:
     - `risk_fee_percentage`
     - `management_fee_monthly_percentage`
     - `application_fee_percentage`
     - `gst_rate`
   - Update calculation logic to include new formulas

2. **Day 13-14: API Endpoint & Testing**
   - Update `POST /api/calculator/` endpoint
   - Add validation for percentage inputs
   - Write comprehensive tests for all calculation scenarios
   - Document the updated API

## Milestone 3: PDF & Document Generation (Week 4)

### 1. Mail Merge and Export as Word
1. **Day 15-16: Template System**
   - Set up template storage in `templates/docs/*.docx`
   - Implement `docxtpl` for template rendering
   - Create context mapping functions

2. **Day 17-18: API Endpoint**
   - Create `POST /api/templates/{template_type}/generate/` endpoint
   - Implement document generation for all required template types
   - Add tests for document generation

### 2. PDF Form Handling
1. **Day 19-20: PDF Form Filling**
   - Implement PDF form field extraction using `pdfrw`
   - Create field mapping logic
   - Add `GET /api/applications/{id}/generate-pdf-filled-form/` endpoint

2. **Day 21: PDF Upload to Application**
   - Create `POST /api/applications/upload-form/` endpoint
   - Implement PDF field extraction and mapping to application model
   - Add validation and error handling

## Milestone 4: Notification & Reminder Enhancements (Week 5)

1. **Day 22-23: Stagnation Reminders** doen
   - Create Celery task `check_stagnant_applications()`
   - Implement notification generation logic
   - Set up daily schedule in Celery Beat

2. **Day 24-25: Note Assignment** done
   - Add `assigned_to` field to Notes model
   - Create migration for database update
   - Implement notification logic for note assignment

3. **Day 26-27: Email Reminders** done 
   - Create `Reminder` model
   - Implement Celery task for checking and sending reminders
   - Add API endpoints for managing reminders
   - User can set automated email reminders to either other team members or client or both (user can choose who the reminder email will be sent to)
   - User can change who the email is sent from (MAYBE POSSBILE NEED TO DOUBLE CHECK WITH
MIKE)
      -Example: Benson asks Ivan to help send an email for Benson to a client. The client will
receive the email with the sender being Benson. When client replies to email it will send
email to Benson NOT Ivan.
## Milestone 5: Application Enhancements (Week 6)

1. **Day 28: Stage Name Updates** Done
   - Update stage choice constants
   - Create migration for mapping old stages to new ones
   - Update serializers and views

2. **Day 29: Product Column** Done
   - Add `product_name` field to application serializer
   - Update API responses to include product information 

3. **Day 30: Loan Extension API** Done
   - Create `POST /api/applications/{id}/extend-loan/` endpoint
   - Implement logic for loan extension and repayment recalculation
   - Add tests for loan extension functionality
   - input fields: new rate, new loan amount, new repayment
## Milestone 6: Additional Features (Week 7-8)

1. **Day 31-32: Duplicate Borrower Detection**
   - Implement fuzzy matching algorithm for borrower data
   - Add validation on borrower creation
   - Create warning system for potential duplicates

2. **Day 33-34: Commission Tracking**
   - Create commission calculation service
   - Implement `/api/brokers/{id}/commission-summary/` endpoint
   - Add tests for commission calculations

3. **Day 35-36: Email Audit Logs**
   - Finalize `SentEmailLog` model implementation
   - Create API endpoint for viewing email logs
   - Add filtering and pagination

4. **Day 37-38: Final Testing & Documentation**
   - Comprehensive integration testing
   - Update API documentation
   - Create user guides for new features

## Milestone 7: Deployment & Handover (Week 8)

1. **Day 39-40: Deployment Preparation**
   - Update Docker configuration for new dependencies
   - Configure Celery and Redis for production
   - Set up secure credential management for DocuSign

2. **Day 41-42: Deployment & Monitoring**
   - Deploy to staging environment
   - Monitor for issues
   - Fix any deployment-related bugs
   - Prepare for production deployment

## Priority Order (Most Important to Least):

1. DocuSign Integration
2. Email Send-As Functionality
3. Calculator API 
4. Mail Merge and Export as Word
5. PDF Form Handling
6. Notification & Reminder Enhancements
7. Application Enhancements
8. Additional Features (Duplicate Detection, Commission Tracking, etc.)
9. Product function
