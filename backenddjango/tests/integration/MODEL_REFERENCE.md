# Model Reference for Integration Testing

This document provides a reference of all model fields for use in integration testing with Factory Boy.

## User Model

```python
# users.models.User
fields = [
    'id', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name', 
    'is_staff', 'is_active', 'date_joined', 'email', 'role', 'phone', 'username', 
    'groups', 'user_permissions'
]

# Related fields
related = [
    'logentry', 'notifications', 'notification_preferences', 'created_applications', 
    'uploaded_documents', 'borrower_profile', 'created_borrowers', 'asset', 
    'liability', 'guarantor', 'branch', 'bdm_profile', 'created_bdms', 
    'broker_profile', 'created_brokers', 'document', 'note', 'fee', 
    'repayment', 'ledger'
]
```

## Borrower Model

```python
# borrowers.models.Borrower
fields = [
    'id', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone', 
    'residential_address', 'mailing_address', 'tax_id', 'marital_status', 
    'residency_status', 'employment_type', 'employer_name', 'employer_address', 
    'job_title', 'employment_duration', 'annual_income', 'other_income', 
    'monthly_expenses', 'bank_name', 'bank_account_name', 'bank_account_number', 
    'bank_bsb', 'referral_source', 'tags', 'notes_text', 'is_company', 
    'company_name', 'company_abn', 'company_acn', 'company_address', 
    'user', 'created_by', 'created_at', 'updated_at'
]

# Related fields
related = [
    'borrower_applications', 'assets', 'liabilities', 'borrower_guarantors', 
    'documents', 'notes'
]
```

## Application Model

```python
# applications.models.Application
fields = [
    'id', 'reference_number', 'stage', 'application_type', 'purpose', 
    'loan_amount', 'loan_term', 'interest_rate', 'repayment_frequency', 
    'product_id', 'estimated_settlement_date', 'broker', 'branch', 'bd', 
    'signed_by', 'signature_date', 'uploaded_pdf_path', 'valuer_company_name', 
    'valuer_contact_name', 'valuer_phone', 'valuer_email', 'valuation_date', 
    'valuation_amount', 'qs_company_name', 'qs_contact_name', 'qs_phone', 
    'qs_email', 'qs_report_date', 'security_address', 'security_type', 
    'security_value', 'created_by', 'created_at', 'updated_at', 
    'borrowers', 'guarantors'
]

# Related fields
related = [
    'app_documents', 'app_fees', 'app_repayments', 'application_guarantors', 
    'documents', 'notes', 'fees', 'repayments', 'ledger_entries'
]
```

## Document Model

```python
# documents.models.Document
fields = [
    'id', 'title', 'description', 'document_type', 'file', 'file_name', 
    'file_size', 'file_type', 'version', 'previous_version', 'application', 
    'borrower', 'created_by', 'created_at', 'updated_at'
]

# Related fields
related = [
    'next_versions'
]
```

## Repayment Model

```python
# applications.models.Repayment
fields = [
    'id', 'application', 'due_date', 'amount', 'status', 'paid_date', 
    'payment_amount', 'invoice', 'notes', 'created_at', 'updated_at'
]
```

## Notification Model

```python
# users.models.Notification
fields = [
    'id', 'user', 'title', 'message', 'notification_type', 'related_object_id', 
    'related_object_type', 'is_read', 'created_at'
]
```

## Broker Model

```python
# brokers.models.Broker
fields = [
    'id', 'name', 'company', 'email', 'phone', 'address', 'branch', 'user', 
    'commission_bank_name', 'commission_account_name', 'commission_account_number', 
    'commission_bsb', 'created_by', 'created_at', 'updated_at'
]

# Related fields
related = [
    'broker_applications', 'bdms'
]
```

## Branch Model

```python
# brokers.models.Branch
fields = [
    'id', 'name', 'address', 'phone', 'email', 'created_by', 'created_at', 
    'updated_at'
]

# Related fields
related = [
    'branch_applications', 'branch_bdms', 'branch_brokers'
]
```

## BDM Model (Business Development Manager)

```python
# brokers.models.BDM
fields = [
    'id', 'name', 'email', 'phone', 'branch', 'user', 'created_by', 
    'created_at', 'updated_at'
]

# Related fields
related = [
    'bdm_applications', 'bdm_brokers'
]
```

## Factory Boy Best Practices

1. **Match field names exactly**: Ensure factory field names match model field names
2. **Handle required fields**: Always include required fields in your base factory
3. **Use LazyAttribute for derived fields**: For fields that depend on other fields
4. **Use SubFactory for related models**: For foreign key relationships
5. **Use post_generation hooks**: For many-to-many relationships
6. **Create specialized factories**: Inherit from base factories for specific scenarios
7. **Use Faker for realistic data**: For names, addresses, emails, etc.
8. **Test your factories**: Ensure they create valid model instances

## Common Factory Patterns

### Creating related objects

```python
class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = Application
    
    # Use SubFactory for foreign keys
    broker = factory.SubFactory(BrokerFactory)
    
    @factory.post_generation
    def borrowers(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for borrower in extracted:
                self.borrowers.add(borrower)
        else:
            # Create a default borrower if none provided
            borrower = BorrowerFactory()
            self.borrowers.add(borrower)
```

### Creating sequences

```python
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
```

### Creating variations

```python
class AdminUserFactory(UserFactory):
    role = 'admin'
    is_staff = True
    is_superuser = True

class ClientUserFactory(UserFactory):
    role = 'client'
    is_staff = False
    is_superuser = False
```
