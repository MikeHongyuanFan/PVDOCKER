You are a senior Django REST Framework test engineer.

I want you to generate a complete Django integration test suite for the Application model based on the following API behavior. It should test both success and failure cases across CRUD operations and custom endpoints.

Requirements:
- Use Django REST Framework's `APITestCase` or `pytest-django` format.
- Include setup logic for authenticated users, brokers, and minimum foreign key requirements (e.g., borrowers, products).
- Use actual expected response data and validate key fields.
- Test all application API endpoints including:
  - `/api/applications/` (GET, POST, filtering, search)
  - `/api/applications/{id}/` (GET, PUT, PATCH, DELETE)
  - `/api/applications/{id}/stage/` (stage update, invalid transitions)
  - `/api/applications/validate-schema/` (valid and invalid input)
  - `/api/applications/create-with-cascade/`
  - `/api/applications/{id}/borrowers/` and `/remove_borrowers/`
  - `/api/applications/{id}/sign/` and `/signature/`
  - `/api/applications/{id}/documents/` and `/upload_document/`
  - `/api/applications/{id}/fees/`, `/add_fee/`
  - `/api/applications/{id}/repayments/`, `/add_repayment/`, `/record_payment/`
  - `/api/applications/{id}/ledger/`

Test coverage expectations:
- Positive case with all required fields
- Negative case with invalid data
- Auth failure (unauthorized)
- Permission failure (wrong user)
- 404 Not Found (nonexistent app)
- 400 Bad Request (validation errors)

Reference this application API spec for your implementation:
- [API part 1]: includes basic CRUD and stage/borrower handling
- [API part 2]: includes schema validation and stage workflows
- [API part 3]: includes document, fee, repayment, ledger

Start by generating `test_application_api.py` with at least 10 structured integration tests covering key flows.
