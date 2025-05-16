
You are a senior Django backend engineer.

**Context:**
I have an existing email service implemented in `users/services.py` using `send_mail`, which:
- Sends plain text emails directly
- Is called from the notification system based on user preferences
- Has password reset handling
- Uses environment variables in `settings_docker.py` for config

**Requirements:**
Refactor and enhance the email system with the following features:

---

### 1. ✅ **Asynchronous Email Sending**
- Replace direct `send_mail` calls with a Celery task
- Create a task `send_email_async` that accepts subject, message, recipients, etc.
- Use `.delay()` in service functions
- Place tasks in `crm_backend/tasks.py`

---

### 2. ✅ **HTML Email Support**
- Modify `send_email_notification` to accept a `template_name` and `context`
- Use `render_to_string` for HTML emails
- Fallback to plain text via `strip_tags`

---

### 3. ✅ **Email Digest Functionality**
- Use fields from `NotificationPreference`: `daily_digest`, `weekly_digest`
- Create two Celery periodic tasks:
  - `send_daily_digest`
  - `send_weekly_digest`
- Aggregate user notifications into email digests (24h for daily, 7d for weekly)
- Use email templates: `emails/daily_digest.html`, etc.

---

### 4. ✅ **Email Log Tracking**
- Create model `EmailLog`:
  ```python
  class EmailLog(models.Model):
      user = models.ForeignKey('users.User', on_delete=models.CASCADE)
      subject = models.CharField(max_length=255)
      sent_at = models.DateTimeField(auto_now_add=True)
      status = models.CharField(max_length=20, choices=[
          ('sent', 'Sent'),
          ('delivered', 'Delivered'),
          ('opened', 'Opened'),
          ('clicked', 'Clicked'),
          ('bounced', 'Bounced'),
          ('failed', 'Failed')
      ], default='sent')
      notification = models.ForeignKey('users.Notification', on_delete=models.SET_NULL, null=True, blank=True)
      message_body = models.TextField(null=True, blank=True)
      email_type = models.CharField(max_length=100, null=True, blank=True)
````

* Log entries in both `send_email_notification` and digest tasks.

---

### 5. ✅ **Error Handling & Retry**

* Use Celery retry logic:

  ```python
  @shared_task(bind=True, max_retries=3)
  def send_email_with_retry(self, ...):
      ...
      raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
  ```

---

### 6. ✅ **Email Testing Mode**

* In dev, capture all emails to a test inbox or local console backend.
* Add `EMAIL_TEST_MODE = True` in dev settings.
* If test mode is enabled, override recipient to a test email (e.g., [test@example.com](mailto:test@example.com)).
* Implement a `preview_email(template_name, context)` dev-only view to render test emails in the browser.

---

### 7. ✅ **Testing Requirements**

Write tests using `pytest` or Django `TestCase` for:

* Email sending via Celery
* HTML rendering logic
* Digest task content generation
* EmailLog creation
* Retry mechanism
* Handling missing email addresses

Use mocks to avoid sending real emails in unit tests.

---

### 8. ✅ **Email Log Export as DOCX**

* Create a service function `export_email_logs_to_docx(log_ids: list[int]) -> BytesIO` using `python-docx`
* For each `EmailLog` entry, include:

  * Subject
  * Recipient (user.email)
  * Sent timestamp
  * Status
  * Email type (if any)
  * Message body (if stored)
* Add proper headings, separators, and formatting
* Create a view (e.g., `download_email_logs`) that:

  * Accepts `GET` query param `?ids=1&ids=2&...`
  * Returns a `.docx` file using `FileResponse`
  * Sets content type to `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
* Use `select_related` for performance

Ensure security (only admins or staff users can access this endpoint if exposed).

---

Please implement the above in a modular, maintainable, and production-ready way. Use logging, error handling, and docstrings throughout.

```