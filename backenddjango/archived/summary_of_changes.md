# Summary of Changes to Reports API OpenAPI Specification

## 1. Schema Definitions
- **Added Repayment Model Definition**: Created a new schema for the Repayment model that includes:
  - `status` field with enum values: `scheduled`, `paid`, `missed`, `partial`
  - `payment_amount` field with appropriate type and description
  - Other relevant fields from the Repayment model

## 2. Endpoint Documentation
- **Updated Base URL**: Changed from `/api` to `/api/v1/reports` to match the actual implementation
- **Enhanced Permission Requirements**: Added explicit mention that all endpoints require the `IsAuthenticated` permission class in the 403 response descriptions and security scheme documentation

## 3. Query Parameters
- **Improved Parameter Documentation**: Enhanced descriptions of existing query parameters to better explain their purpose and usage
- **Parameter Validation**: Added enum values and format specifications where appropriate

## 4. Response Structures
- **Updated Active Stages List**: Added comprehensive list of active stages in the ApplicationStatusReport schema to match the implementation:
  ```
  inquiry, sent_to_lender, funding_table_issued, iloo_issued, iloo_signed, 
  commitment_fee_paid, app_submitted, valuation_ordered, valuation_received, 
  more_info_required, formal_approval, loan_docs_instructed, loan_docs_issued, 
  loan_docs_signed, settlement_conditions
  ```
- **Added Placeholder Values Note**: Added explicit documentation that the `avg_time_in_stage` field contains placeholder values (all zeros) in the current implementation

## 5. Implementation Details
- **Added Calculation Methods**: Enhanced descriptions to explain how metrics are calculated:
  - Compliance rates: `paid_on_time / total_repayments * 100`
  - Payment rates: `amount_paid / amount_due * 100`
  - Conversion rates: Various formulas documented
- **Added Error Handling Information**: Added notes about division by zero handling in various rate calculations

## 6. Examples and Documentation
- **Updated Example Values**: Aligned example values with the actual implementation
- **Enhanced Field Descriptions**: Added more detailed descriptions for fields, including:
  - How they are calculated
  - What they represent
  - Source fields from the database

## 7. Security and Authentication
- **Enhanced Authentication Documentation**: Added more details about the authentication mechanisms:
  - Specified that JWT is the primary authentication method
  - Mentioned that Django REST Framework also supports other authentication methods
- **Added Permission Requirements**: Clarified that all endpoints require the `IsAuthenticated` permission class

These improvements make the OpenAPI document more accurately reflect the actual implementation and provide better guidance for API consumers.