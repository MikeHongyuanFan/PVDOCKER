### Product api services check list 
## Functions:##
1. Servers as a data input and output api end point, where the users is able to: 
 - Input related information to create products types.
 - Edit product information 
 - Perform product delete action.

## Relationships##
 - Product connnect to application, one application can have 1  ? products?(Mutipual application)
 - One product can be owned by mutipual applications? (Yes)
 - Relationship to borrowers (Connect Borrower to many product)
 - Relationship to brokers non 
 - Relationship to branches (non)
 - Relationship to document (yes one document have mutipual product)
 
## Input fields##
 
List of names. 
### Calculator### 

The Funding Calculator system enhances the CRM Loan Management System by providing:
- Automatic calculation of application funding at the time of creation.
- Editable calculation inputs during application updates.
- A complete history log of all funding recalculations for auditing and compliance.
## Relationships##
# Following Shows Create Application with Related Entities

- **Request Example**:
  ```
  POST /api/applications/create-with-cascade/
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json

  {
    "loan_amount": 500000.00,
    "loan_term": 30,
    "interest_rate": 4.5,
    "purpose": "Home purchase",
    "repayment_frequency": "monthly",
    "application_type": "residential",
    "product_id": "PROD001",
    "estimated_settlement_date": "2023-05-30",
    "stage": "inquiry",
    "broker": 42,
    "bd": 15,
    "branch": 7,
    "security_address": "123 Main St, Anytown",
    "security_type": "residential",
    "security_value": 650000.00,

    Automaticly input Calculator action: Receive data input from previous stage? or manually input again? 

    "borrowers": [
      {
        "first_name": "Michael",
        "last_name": "Johnson",
        "email": "michael@example.com",
        "phone": "+1234567890",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1980-05-15",
        "employment_type": "full_time",
        "annual_income": 120000.00
      },
      {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@example.com",
        "phone": "+1234567891",
        "residential_address": "456 Oak St, Anytown",
        "date_of_birth": "1982-08-20",
        "employment_type": "part_time",
        "annual_income": 60000.00
      }
    ],
    "guarantors": [
      {
        "guarantor_type": "individual",
        "first_name": "Robert",
        "last_name": "Smith",
        "email": "robert@example.com",
        "phone": "+1234567892",
        "address": "789 Pine St, Anytown",
        "relationship_to_borrower": "parent"
      }
    ],
    "company_borrowers": [
      {
        "company_name": "Johnson Enterprises",
        "abn": "12345678901",
        "acn": "123456789",
        "business_address": "101 Business Ave, Anytown",
        "contact_name": "Michael Johnson",
        "contact_email": "contact@johnsonenterprises.com",
        "contact_phone": "+1234567893"
      }
    ]
  }
  Finally output to Application detail api service
  ```
  ### What we need to comform is in which step of application creation work flow will the calculation action be, and we need to couble check and make sure the input fields of application be accurate.###



### Email Send-As Functionality
#### Objective:
Allow users to send emails that appear from another user (e.g., assistants sending on behalf).

#### Strategy:
1. **Backend Changes**
   - Extend email service to support:
     - `from_user`: sender displayed
     - `actual_sender`: SMTP sender
     - `reply_to`: user email who should receive replies

2. **Model Update**
   - Add metadata to store send-as history (e.g., `SentEmailLog`)

3. **Security Controls**
   - Allow only authorized roles to send-as another user (e.g., assistant)

4. **Endpoint**: `POST /api/emails/send/`
   - Input: `subject`, `body`, `recipient`, `from_user_id`, `reply_to_id`
   - Validations: user permissions, email format

5. **UI**
   - Dropdown on email form to select sender identity (if permitted) 

### Where for this api service, we need to verify with client is this API functional design is correctly implemented the client's needs.###


##  Application Missing features

### Stage Name Updates
What will be the new updated stage names? 
Sent to Lender/ Funding Table Issued/ ILOO Issued/ ILOO Signed, Commitment Fee Paid/ App Submitted/ Valuation Ordered/ Valuation Received/ More Info Required/ Formal Approval/ Loan Docs Instructed/ Loan Docs Issued/ Loan Docs Signed/ Settlement Conditions/ Settled / Closed
### Email Generate docs file function
What we need to check with client is: 
- The generated document should be downloaded YES? Or store in the system? YES

