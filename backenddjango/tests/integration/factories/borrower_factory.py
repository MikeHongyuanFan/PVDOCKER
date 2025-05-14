"""
Factory for Borrower model.
"""

import factory
import random
from decimal import Decimal
from factory.django import DjangoModelFactory
from borrowers.models import Borrower
from .user_factory import UserFactory


class BorrowerFactory(DjangoModelFactory):
    """
    Base factory for Borrower model.
    """
    
    class Meta:
        model = Borrower
        django_get_or_create = ('email',)
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f'{obj.first_name.lower()}.{obj.last_name.lower()}@example.com')
    phone = factory.Faker('phone_number')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    residential_address = factory.Faker('street_address')
    mailing_address = factory.LazyAttribute(lambda obj: obj.residential_address)
    tax_id = factory.Sequence(lambda n: f'TAX{n:06d}')
    marital_status = factory.Iterator(['Single', 'Married', 'Divorced', 'Widowed'])
    residency_status = factory.Iterator(['Citizen', 'Permanent Resident', 'Temporary Resident'])
    employment_type = factory.Iterator(['Full Time', 'Part Time', 'Self Employed', 'Unemployed'])
    employer_name = factory.Faker('company')
    employer_address = factory.Faker('street_address')
    job_title = factory.Faker('job')
    employment_duration = factory.LazyFunction(lambda: random.randint(1, 240))  # months
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(30000, 200000))))
    other_income = factory.LazyFunction(lambda: Decimal(str(random.randint(0, 50000))))
    monthly_expenses = factory.LazyFunction(lambda: Decimal(str(random.randint(1000, 5000))))
    bank_name = factory.Faker('company')
    bank_account_name = factory.LazyAttribute(lambda obj: f'{obj.first_name} {obj.last_name}')
    bank_account_number = factory.Sequence(lambda n: f'{random.randint(100000, 999999):06d}')
    bank_bsb = factory.Sequence(lambda n: f'{random.randint(100000, 999999):06d}')
    referral_source = factory.Iterator(['Website', 'Broker', 'Friend', 'Advertisement'])
    tags = factory.List([factory.Faker('word') for _ in range(3)])
    notes_text = factory.Faker('paragraph')
    is_company = False
    created_by = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)


class CompanyBorrowerFactory(BorrowerFactory):
    """
    Factory for company borrowers.
    """
    
    is_company = True
    company_name = factory.Faker('company')
    company_abn = factory.Sequence(lambda n: f'ABN{n:011d}')
    company_acn = factory.Sequence(lambda n: f'ACN{n:09d}')
    company_address = factory.Faker('street_address')


class HighIncomeProfileFactory(BorrowerFactory):
    """
    Factory for borrowers with high income.
    """
    
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(200001, 1000000))))
    employment_type = 'Full Time'
    employment_duration = factory.LazyFunction(lambda: random.randint(24, 240))  # months


class LowIncomeProfileFactory(BorrowerFactory):
    """
    Factory for borrowers with low income.
    """
    
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(10000, 30000))))
    employment_type = factory.Iterator(['Part Time', 'Unemployed'])
    employment_duration = factory.LazyFunction(lambda: random.randint(0, 12))  # months


class SelfEmployedProfileFactory(BorrowerFactory):
    """
    Factory for self-employed borrowers.
    """
    
    employment_type = 'Self Employed'
    employer_name = factory.LazyAttribute(lambda obj: f'{obj.first_name}\'s Business')
    employment_duration = factory.LazyFunction(lambda: random.randint(12, 240))  # months
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(50000, 500000))))


class RetiredProfileFactory(BorrowerFactory):
    """
    Factory for retired borrowers.
    """
    
    employment_type = 'Retired'
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(20000, 100000))))
    other_income = factory.LazyFunction(lambda: Decimal(str(random.randint(10000, 50000))))
    date_of_birth = factory.Faker('date_of_birth', minimum_age=60, maximum_age=90)


class GuarantorProfileFactory(BorrowerFactory):
    """
    Factory for borrowers who are guarantors.
    """
    
    employment_type = 'Full Time'
    annual_income = factory.LazyFunction(lambda: Decimal(str(random.randint(80000, 300000))))
    employment_duration = factory.LazyFunction(lambda: random.randint(36, 240))  # months
