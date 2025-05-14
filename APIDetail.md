# API Documentation for CRM Loan Management System

This document provides detailed information about the API endpoints available in the CRM Loan Management System. The API is built using Django REST Framework and follows RESTful principles.

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints, you need to include the JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Authentication Endpoints

- **POST /api/users/login/**: Obtain JWT token by providing username and password
- **POST /api/users/refresh/**: Refresh JWT token
- **POST /api/users/register/**: Register a new user
- **GET /api/users/me/**: Get current user information

## Applications

Applications are the core entity in the system, representing loan applications.

### Endpoints

- **GET /api/applications/enhanced-applications/**: Get enhanced application list with additional fields
- **POST /api/applications/**: Create a new application
- **GET /api/applications/{id}/**: Get application details
- **PUT /api/applications/{id}/**: Update application
- **PATCH /api/applications/{id}/**: Partially update application
- **DELETE /api/applications/{id}/**: Delete application
- **POST /api/applications/{id}/status/**: Update application status
- **GET /api/applications/{id}/documents/**: List application documents
- **POST /api/applications/{id}/documents/**: Upload document to application
- **GET /api/applications/{id}/notes/**: List application notes
- **POST /api/applications/{id}/notes/**: Add note to application
- **GET /api/applications/{id}/fees/**: List application fees
- **POST /api/applications/{id}/fees/**: Add fee to application
- **GET /api/applications/{id}/repayments/**: List application repayments
- **POST /api/applications/{id}/repayments/**: Add repayment to application
- **GET /api/applications/{id}/ledger/**: Get application ledger entries

## Borrowers

Borrowers represent individuals or companies applying for loans.

### Endpoints

- **GET /api/borrowers/**: List all borrowers
- **POST /api/borrowers/**: Create a new borrower
- **GET /api/borrowers/{id}/**: Get borrower details
- **PUT /api/borrowers/{id}/**: Update borrower
- **PATCH /api/borrowers/{id}/**: Partially update borrower
- **DELETE /api/borrowers/{id}/**: Delete borrower
- **GET /api/borrowers/{id}/applications/**: List borrower applications
- **GET /api/borrowers/{id}/assets/**: List borrower assets
- **POST /api/borrowers/{id}/assets/**: Add asset to borrower
- **GET /api/borrowers/{id}/liabilities/**: List borrower liabilities
- **POST /api/borrowers/{id}/liabilities/**: Add liability to borrower
- **GET /api/borrowers/{id}/guarantors/**: List borrower guarantors
- **POST /api/borrowers/{id}/guarantors/**: Add guarantor to borrower
- **GET /api/borrowers/{id}/financial-summary/**: Get borrower financial summary

## Brokers

Brokers represent intermediaries who submit loan applications on behalf of borrowers.

### Endpoints

- **GET /api/brokers/**: List all brokers
- **POST /api/brokers/**: Create a new broker
- **GET /api/brokers/{id}/**: Get broker details
- **PUT /api/brokers/{id}/**: Update broker
- **PATCH /api/brokers/{id}/**: Partially update broker
- **DELETE /api/brokers/{id}/**: Delete broker
- **GET /api/brokers/{id}/applications/**: List broker applications
- **GET /api/brokers/branches/**: List all branches
- **POST /api/brokers/branches/**: Create a new branch
- **GET /api/brokers/branches/{id}/**: Get branch details
- **PUT /api/brokers/branches/{id}/**: Update branch
- **DELETE /api/brokers/branches/{id}/**: Delete branch
- **GET /api/brokers/bdms/**: List all BDMs (Business Development Managers)
- **POST /api/brokers/bdms/**: Create a new BDM
- **GET /api/brokers/bdms/{id}/**: Get BDM details
- **PUT /api/brokers/bdms/{id}/**: Update BDM
- **DELETE /api/brokers/bdms/{id}/**: Delete BDM

## Documents

Documents represent files attached to applications, borrowers, or other entities.

### Endpoints

- **GET /api/documents/**: List all documents
- **POST /api/documents/**: Upload a new document
- **GET /api/documents/{id}/**: Get document details
- **PUT /api/documents/{id}/**: Update document metadata
- **DELETE /api/documents/{id}/**: Delete document
- **GET /api/documents/{id}/download/**: Download document file
- **POST /api/documents/{id}/versions/**: Create a new version of a document
- **GET /api/documents/{id}/versions/**: List document versions

## Products

Products represent loan products offered by the company.

### Endpoints

- **GET /api/products/**: List all products
- **POST /api/products/**: Create a new product
- **GET /api/products/{id}/**: Get product details
- **PUT /api/products/{id}/**: Update product
- **PATCH /api/products/{id}/**: Partially update product
- **DELETE /api/products/{id}/**: Delete product
- **GET /api/products/{id}/applications/**: List applications for a product

## Reports

Reports provide aggregated data and analytics.

### Endpoints

- **GET /api/reports/repayment-compliance/**: Get repayment compliance report
- **GET /api/reports/application-volume/**: Get application volume report
- **GET /api/reports/application-status/**: Get application status report

## Reminders

Reminders are notifications scheduled for future delivery.

### Endpoints

- **GET /api/reminders/**: List all reminders
- **POST /api/reminders/**: Create a new reminder
- **GET /api/reminders/{id}/**: Get reminder details
- **PUT /api/reminders/{id}/**: Update reminder
- **DELETE /api/reminders/{id}/**: Delete reminder
- **POST /api/reminders/{id}/send-now/**: Send reminder immediately

## Notifications

Notifications inform users about events in the system.

### Endpoints

- **GET /api/users/notifications/**: List user notifications
- **GET /api/users/notifications/count/**: Get unread notification count
- **POST /api/users/notifications/{id}/read/**: Mark notification as read
- **POST /api/users/notifications/read-all/**: Mark all notifications as read

## WebSockets

The system uses WebSockets for real-time notifications. WebSocket connections are authenticated using JWT tokens.

### WebSocket Endpoints

- **ws://localhost:8000/ws/notifications/**: Notifications WebSocket endpoint

## Data Models

The API is built around the following core data models:

- **User**: System users with different roles (admin, staff, broker, borrower)
- **Application**: Loan applications with status workflow
- **Borrower**: Individual or company applying for a loan
- **Guarantor**: Individual or company guaranteeing a loan
- **Broker**: Intermediary submitting applications
- **Document**: Files attached to applications or other entities
- **Product**: Loan products offered by the company
- **Fee**: Fees associated with applications
- **Repayment**: Scheduled repayments for loans
- **Notification**: System notifications for users
- **Reminder**: Scheduled reminders for future actions

## Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error responses include a JSON body with error details:

```json
{
  "detail": "Error message",
  "code": "error_code",
  "errors": {
    "field_name": ["Error message for field"]
  }
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- **page**: Page number (default: 1)
- **page_size**: Number of items per page (default: 10)

Paginated responses include:

```json
{
  "count": 100,
  "next": "http://api.example.com/items/?page=3",
  "previous": "http://api.example.com/items/?page=1",
  "results": [
    // items
  ]
}
```

## Filtering and Sorting

Many list endpoints support filtering and sorting:

- **Filtering**: Use query parameters matching field names (e.g., `?status=approved`)
- **Sorting**: Use the `ordering` parameter (e.g., `?ordering=created_at` or `?ordering=-created_at` for descending)

## API Versioning

The API is versioned through the URL path. The current version is v1, which is implicit in the API paths.

## Rate Limiting

API requests are rate-limited to prevent abuse. The limits are:

- **Authenticated users**: 100 requests per minute
- **Anonymous users**: 20 requests per minute

Rate limit headers are included in responses:

- **X-RateLimit-Limit**: Maximum requests per period
- **X-RateLimit-Remaining**: Remaining requests in current period
- **X-RateLimit-Reset**: Seconds until rate limit reset
