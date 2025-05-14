# CRM Loan Management System

A comprehensive CRM system for loan applications with fully synchronized frontend and backend development.

## Project Structure

- **Backend:** Django + Django REST Framework
- **Frontend:** Vue 3 + Pinia (state), Axios (API)

## Tech Stack

### Backend
- Django 4.x
- Django REST Framework
- PostgreSQL
- Celery + Redis (background tasks)
- SimpleJWT (auth)
- Swagger (API docs)
- Docker & Docker Compose

### Frontend
- Vue 3 + Composition API
- Vue Router
- Pinia (store)
- Axios
- TailwindCSS
- Vite

## Getting Started with Docker (Recommended)

Run the entire stack with Docker Compose:
```
docker-compose up
```

This will start:
- Django backend on port 8000
- Vue frontend on port 3000
- PostgreSQL database on port 5432
- Redis on port 6379
- Celery worker for background tasks

### Access the applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin interface: http://localhost:8000/admin/
- API documentation: http://localhost:8000/swagger/

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backenddjango
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontendVUE
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

## API Documentation

API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## API Relationships

The API relationships between the frontend and backend are documented in [APIRelationship.md](APIRelationship.md). This document outlines:

- Authentication flow between frontend and backend
- Application management API endpoints and their frontend counterparts
- Borrower, broker, and document management API connections
- Real-time notification system using WebSockets
- Data validation and security measures

## Project Structure

### Backend Structure
```
backenddjango/
├── applications/     # Loan applications app
├── borrowers/        # Borrower management app
├── brokers/          # Broker management app
├── crm_backend/      # Main project settings
├── documents/        # Document management app
├── products/         # Product management app
├── users/            # User authentication app
├── tests/            # Test suite
│   ├── integration/  # Integration tests
│   └── unit/         # Unit tests
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── requirements.txt  # Python dependencies
```

### Frontend Structure
```
frontendVUE/
├── src/
│   ├── assets/       # Static assets
│   ├── components/   # Reusable Vue components
│   ├── router/       # Vue Router configuration
│   ├── services/     # API services
│   │   └── __tests__/ # Service tests
│   ├── store/        # Pinia stores
│   ├── views/        # Page components
│   ├── App.vue       # Root component
│   └── main.js       # Entry point
├── .env              # Environment variables
└── package.json      # NPM dependencies
```

## Features

- User authentication with role-based permissions
- Loan application management with multi-step form process
- Borrower and guarantor information management
- Document generation and management
- Product management with application, document, and borrower associations
- Fee and repayment tracking
- Comprehensive notification system for application status changes
- Electronic signature processing and validation
- Transaction-based cascade operations for data integrity
- Reporting and analytics
- Real-time notifications via WebSockets

## Testing

### Backend Tests

Run backend tests with:
```
cd backenddjango
python manage.py test tests
```

The backend test suite includes:
- Unit tests for models, serializers, and services
- Integration tests for API endpoints
- Authentication and permission tests
- API connection tests

### Frontend Tests

Run frontend tests with:
```
cd frontendVUE
npm run test
```

The frontend test suite includes:
- API service tests
- Store tests
- Component tests
- WebSocket connection tests

## Development Workflow

This project follows an agile development process with the following phases:

1. Project Bootstrapping (Completed)
   - Backend: Django project setup, apps creation, PostgreSQL connection, CORS setup, Docker configuration
   - Frontend: Vue project setup, folder structure, router setup, store setup, API service configuration

2. Authentication & Role Setup (Completed)
   - User model with role-based permissions
   - JWT authentication integration
   - Permission classes for API endpoints

3. Application Core Development (Completed)
   - Core models for applications, borrowers, and documents
   - Basic CRUD operations for all entities
   - Relationship establishment between entities
   - Multi-step application form with validation
   - Application status workflow management
   - Transaction-based cascade operations
   - Electronic signature processing

4. Application Detail & Management (Completed)
   - Application detail page with tabbed interface
   - Notes and reminders system
   - Document management
   - Repayment schedule tracking
   - Ledger and fee management

5. Notifications & Background Jobs (Completed)
   - User notification system for status changes
   - Email notifications via background tasks
   - Real-time notifications via WebSockets
   - Application event tracking

6. Reporting & Analytics (Completed)
   - Repayment compliance reports
   - Application volume reports
   - Application status reports
   - Visual charts and filters

7. API Relationship Documentation (Completed)
   - Documentation of API connections
   - Test suite for API connections
   - Verification of frontend-backend integration

8. Deployment & DevOps (Planned)
