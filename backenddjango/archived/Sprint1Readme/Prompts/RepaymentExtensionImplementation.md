
### Repayment extension prompt
> Hi Q Chat, I need help implementing a new API endpoint for our Django-based CRM Loan Management System:
>
> ### ✅ Endpoint:
> `POST /api/applications/{id}/extend-loan/`
>
> ### 🧩 Purpose:
> Extend a loan by:
> - Updating the loan amount, interest rate, and repayment amount
> - Regenerating repayment schedules
> - Ensuring repayment tracking and notification fields remain consistent with the API standard
>
> ### 🔧 Input Payload:
> ```json
> {
>   "new_rate": 7.25,
>   "new_loan_amount": 850000,
>   "new_repayment": 15000
> }
> ```
>
> ### ✅ Implementation Requirements:
> 1. Update the `Application` model fields: `loan_amount`, `interest_rate`, and `repayment_amount`.
> 2. **Delete or archive existing repayments** under `/api/applications/{id}/repayments/`
> 3. **Regenerate new repayments** using the same schema as `/api/applications/{id}/add-repayment/`, reusing repayment logic (do not duplicate).
> 4. Repayments must retain:
>    - `status` (`scheduled`, `paid`, `overdue_X_days`, etc.)
>    - `reminder_sent`, `overdue_3_day_sent`, `overdue_7_day_sent`, `overdue_10_day_sent`
> 5. Repayments should be visible via:
>    - `/api/documents/repayments/`
>    - `/api/applications/{id}/repayments/`
> 6. Ensure compatibility with:
>    - `mark-paid` endpoint: `/api/documents/repayments/{id}/mark-paid/`
>    - ledger auto-update: `/api/documents/applications/{application_id}/ledger/`
> 7. Add test cases for:
>    - Successful extension
>    - Invalid/missing fields
>    - Old repayments handled properly
>
> ### 🧠 Optional:
> - Log the change in a `LoanExtension` model if present.
> - Trigger optional notification through `/api/users/notifications/` or reminder note via `/api/documents/notes/` if configured.
>
> ### ⚠️ Validate compatibility with:
> - Repayment APIs under `/api/documents/repayments/`
> - Reminder behavior (`remind_date`, `reminder_sent`, etc.)
> - Application update logic under `/api/applications/{id}/`
>
> Please generate:
> - Serializer
> - View (DRF)
> - Reuse repayment scheduling utility
> - Unit test function
> - Ledger or reminder update trigger (if applicable)

---
