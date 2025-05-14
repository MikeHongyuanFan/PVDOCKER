# Detailed Implementation Plan for Missing & New API Services

## 1. 📤 DocuSign Integration & Email Send-as Functionality

### 1.1 DocuSign Integration
#### Objective:
Enable users to send documents to clients for e-signature via DocuSign.

#### Steps:
1. **DocuSign Developer Account Setup**
   - Create DocuSign developer account.
   - Generate integration key, secret, and configure redirect URIs.
   User ID 0500040d-c49a-453b-95dd-40302fd1bdca
   API accountID b23f1b1d-e370-43ec-a8e6-1533d837ec0a
Integration key:783bcc77-f364-4d22-800d-f988e9b2b20e	
secret key: ed6ed069-7ef8-469c-b3ba-2f2dbe2f0d13
Account base URL: https://demo.docusign.net
2. **Backend Integration**
   - Install SDK: `docusign-esign` Python package.
   - Create `EnvelopeService` to:
     - Authenticate with DocuSign (OAuth).
     - Create envelope with document and signer.
     - Define recipient roles and fields (e.g., signHere).
     - Send the envelope and store `envelope_id`.

3. **Endpoint**: `POST /api/documents/{id}/send-for-signature/`
   - Input: `signer_name`, `signer_email`, `message`
   - Output: DocuSign envelope ID and status

4. **Webhook** (Optional)
   - Receive DocuSign status updates (completed, declined, etc.)
   - Endpoint: `POST /api/documents/docusign-webhook/`

5. **UI**
   - Add "Send for Signature" button on document detail page
   - Track status: sent, signed, rejected

---

### 1.2 Email Send-As Functionality
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

---

## 2. 📩 Reminder & Notification Enhancements

### 2.1 Automated Stagnation Reminders
- **Celery Task**: `check_stagnant_applications()`
  - Runs daily
  - Queries applications with `stage_last_updated > X days ago`
  - Sends notification and email to assigned BDM

### 2.2 Assign Notes to Team Member
- Add `assigned_to` field in Notes model (FK to `User`)
- On assignment, create in-app notification: `Note assigned to you by {creator}`
- **UI**: Dropdown to assign note; assigned users see a filter "Assigned to me"

### 2.3 Email Reminders to Client/Team
- Add `Reminder` model:
  ```python
  class Reminder(models.Model):
      recipient_type = models.CharField(choices=["client", "bdm", "broker", "custom"])
      send_datetime = models.DateTimeField()
      email_body = models.TextField()
      subject = models.CharField()
      created_by = models.ForeignKey(User)
  ```
- Celery Beat job checks for due reminders and sends emails
- UI: Reminder scheduler with recipient dropdowns

### 2.4 Reminder Letter Templates
- Use Jinja2/docxtpl to render Word (.docx) from predefined templates
- Endpoint: `/api/templates/{type}/generate/`
  - Input: `application_id`, `type`
  - Output: Word file download URL

---

## 3. Missing Calculator API 
For detail information, check; 
/Users/hongyuanfan/Downloads/lianV3-501a294797023b7f3fa802ddb963f1a4b1577785/backenddjango/NewFeatureCalculator.md 

## 4. Missing Mail Merge and Export as Word

### Template System:
- Store templates in DB or `templates/docs/*.docx`
- Use `docxtpl` or `python-docx` for dynamic merging

### Endpoint: `POST /api/templates/{template_type}/generate/`
- Input: `application_id`, `borrower_id`, etc.
- Process:
  - Fetch context
  - Fill .docx
  - Save file and return URL

### Template Types:
- Indicative Letter
- Settlement Letter
- Reminder Letter
- Renewal Letter
- Extension Letter
- Discharge Letter
- Product List

---

## 5. 📊 Application Missing features

### 5.1 Stage Name Updates
- Update enum/stage choice constants globally
- Migrate existing data to map old stages to new ones

### 5.2 Product Column in Application Table
- Add `product_name` field to serializer
- Display in frontend application table

---

## 6. 📊 Other Missing Features (Backlog)

### 6.1 Loan Extension API
- Endpoint: `POST /api/applications/{id}/extend-loan/`
- Fields: `new_term`, `new_rate`, `new_amount`
- Auto-generate repayment schedule

### 6.2 Duplicate Borrower Detection
- On create, check for fuzzy match of name, email, DOB
- Warn or block creation

### 6.3 Commission Tracking
- Track commission payout via `/api/brokers/{id}/commission-summary/`
- Link to fees table and payment records

### 6.4 Email Audit Logs
- Model: `SentEmailLog`
- Track `to`, `from`, `reply_to`, `subject`, `sent_at`, `status`

---

## 🚀 Deployment Notes
- Celery and Redis required for scheduled tasks
- Add background queue runner in production
- Configure secure DocuSign credentials
- Enable template upload & access permission control

---

Let me know if you want this turned into Django code or a Swagger API spec next.

