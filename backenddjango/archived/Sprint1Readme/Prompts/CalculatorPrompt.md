You are a senior backend engineer familiar with Django, REST APIs, and financial application workflows.

I need you to implement the following system: **Funding Calculator for a CRM Loan Management System**.

The system must support:
- Funding calculation at application creation
- Editable funding parameters during updates
- Full calculation history stored for auditing

Below is the full system design, database schema, input fields, calculation logic, endpoint list, and workflows.

Your task:
1. Confirm if the system design is **feasible and complete**.
2. Highlight any **missing implementation details** I should add.
3. Suggest any **performance, security, or API structure improvements**.
4. Optionally, start generating the **Django models, serializers, views, and calculation service layer** code if the design is ready.

Use standard Django best practices and ensure all historical records are version-safe and auditable.

---

# 📄 Funding Calculator System Design and Workflow Document

---

## 1. Overview

The Funding Calculator system enhances the CRM Loan Management System by providing:
- Automatic calculation of application funding at the time of creation.
- Editable calculation inputs during application updates.
- A complete history log of all funding recalculations for auditing and compliance.

This ensures transparency, traceability, and operational accuracy across loan applications.

---

## 2. Entities and Database Models

### 2.1 Funding Calculation History Model

| Field | Type | Description |
|:--|:--|:--|
| `id` | integer (auto-increment) | Unique record ID |
| `application` | ForeignKey → Application | Links to the associated application |
| `calculation_input` | JSON | Full set of manual input fields used during calculation |
| `calculation_result` | JSON | Computed funding breakdown (all fees, funds available) |
| `created_by` | ForeignKey → User | User who performed the calculation |
| `created_at` | datetime | Timestamp when the calculation was made |

✅ All recalculations create a **new record** (no overwriting).

---

## 3. Input Fields for Calculation

| Field Name | Source | Required? | Notes |
|:--|:--|:--|:--|
| Loan Amount | Application | ✅ | Auto from application create payload |
| Loan Term (months) | Application | ✅ | Auto from application |
| Interest Rate (Annual %) | Application | ✅ | Auto from application |
| Security Value | Application | ✅ | Auto from application |
| Establishment Fee Rate (%) | Manual Input | ✅ | Input manually |
| Capped Interest Months | Manual Input | ✅ | Input manually (default 9 if not provided) |
| Monthly Line Fee Rate (%) | Manual Input | ✅ | Input manually |
| Brokerage Fee Rate (%) | Manual Input | ✅ | Input manually |
| Application Fee ($) | Manual Input | ✅ | Input manually |
| Due Diligence Fee ($) | Manual Input | ✅ | Input manually |
| Legal Fee Before GST ($) | Manual Input | ✅ | Input manually |
| Valuation Fee ($) | Manual Input | ✅ | Input manually |
| Monthly Account Fee ($) | Manual Input | ✅ | Input manually |
| Working Fee ($) | Manual Input | Optional | Default to 0 if blank |

---

## 4. Calculation Logic

| Fee | Formula |
|:--|:--|
| Establishment Fee | `Loan Amount × (Establishment Fee Rate ÷ 100) × 1.1 (GST)` |
| Capped Interest | `Loan Amount × (Interest Rate ÷ 12 ÷ 100) × Capped Interest Months` |
| Line Fee | `Loan Amount × (Monthly Line Fee Rate ÷ 100) × 14` |
| Brokerage Fee | `Loan Amount × (Brokerage Fee Rate ÷ 100) × 1.1 (GST)` |
| Legal Fee (with GST) | `Legal Fee Before GST × 1.1` |
| Application Fee | As provided |
| Due Diligence Fee | As provided |
| Valuation Fee | As provided |
| Monthly Account Fee | As provided |
| Working Fee | As provided or default 0 |

Final outputs:

```plaintext
Total Fees = sum of all fees
Funds Available = Security Value - Total Fees
```

---

## 5. API Endpoints Involved

| API | Method | Purpose |
|:--|:--|:--|
| `/api/applications/` | POST | Create basic application (loan amount, term, interest rate, security value) |
| `/api/applications/create-with-cascade/` | POST | Create application + borrowers/guarantors in one shot |
| `/api/applications/{id}/funding-calculation/` | POST | Create/update current funding calculation (and create new history) |
| `/api/applications/{id}/funding-calculation-history/` | GET | Retrieve funding calculation history list for audit trail |

---

## 6. Workflow Design

### 6.1 During Application Creation
- User fills basic application form (loan amount, interest rate, term, security address, etc.).
- User also **manually inputs** funding calculator fields (fees and rates).
- Backend:
  1. Saves Application record.
  2. Immediately calls internal funding calculation function.
  3. Stores:
     - Funding result into Application model (`funding_result` field).
     - Initial FundingCalculationHistory record.

✅ Funding information is ready right after application created.

---

### 6.2 During Application Edit
- User opens Application Edit page.
- Funding section shows:
  - Current stored funding result
  - Editable form prefilled with last input values.
- User can adjust any manual fields (e.g., establishment fee %, brokerage %, legal fee amount).
- Backend:
  1. Recalculate funding based on new inputs.
  2. Overwrite the `funding_result` JSON field in Application.
  3. Create **a new FundingCalculationHistory record** with:
     - New input
     - New output
     - `created_by = current user`
     - `created_at = now()`

✅ No old data lost — every edit has permanent history.

---

### 6.3 Viewing Calculation History
- On Application Detail/Edit page, add a **"Funding History"** section:
  - Shows all past calculations:
    - Date of calculation
    - Who made the change
    - Loan amount
    - Manual input summary
    - Final funds available
  - Allow drilling down to see full fee breakdown per version.

✅ Supports internal audits, compliance checks, or rollback discussions.

---

## 7. Data Flow Summary

```plaintext
Application Create (POST)
    ↓
Funding Inputs Provided
    ↓
Funding Calculator Called
    ↓
Funding Result Saved to Application
    ↓
Initial FundingCalculationHistory Created
```

```plaintext
Application Edit (PATCH)
    ↓
User Adjusts Funding Inputs
    ↓
Funding Calculator Called
    ↓
Funding Result Overwritten in Application
    ↓
New FundingCalculationHistory Created
```

---

## 8. Error Handling

| Situation | Behavior |
|:--|:--|
| Missing required input | Return 400 Bad Request with field errors |
| Loan Amount ≤ 0 | Validation error |
| Security Value ≤ 0 | Validation error |
| Fees negative or missing | Validation error |
| User unauthorized | Return 401 Unauthorized |

✅ Validation must happen **before** any calculation starts.

---

# ✅ Final Summary Table

| Item | Value |
|:--|:--|
| Calculator integrated into | Application Create + Edit |
| Edit Funding Inputs Later? | Yes |
| Store Edit History? | Yes, every recalculation saved |
| Track User and Time? | Yes |
| Viewable on Application Page? | Yes |
| Data Loss? | No (full versioning kept) |

---

# 📄 Funding Calculator System Design and Workflow Document

[PASTE THE FULL DOCUMENT YOU JUST PROVIDED HERE]

--- END SYSTEM DESIGN ---

Start by reviewing for completeness, then proceed to implementation suggestions.
