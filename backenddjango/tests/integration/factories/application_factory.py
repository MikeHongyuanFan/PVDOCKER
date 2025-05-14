"""
Factory for Application model.
"""

import factory
import random
from decimal import Decimal
from datetime import timedelta
from factory.django import DjangoModelFactory
from applications.models import Application
from .user_factory import UserFactory
from .borrower_factory import BorrowerFactory
from .broker_factory import BrokerFactory, BranchFactory, BDMFactory


class ApplicationFactory(DjangoModelFactory):
    """
    Base factory for Application model.
    """
    
    class Meta:
        model = Application
    
    reference_number = factory.Sequence(lambda n: f'APP-{n:06d}')
    stage = 'draft'
    application_type = factory.Iterator(['Standard', 'Express', 'Premium'])
    purpose = factory.Iterator(['Purchase', 'Refinance', 'Construction', 'Investment'])
    loan_amount = factory.LazyFunction(lambda: Decimal(str(random.randint(10000, 500000))))
    loan_term = factory.Iterator([12, 24, 36, 48, 60])
    interest_rate = factory.LazyFunction(lambda: Decimal(str(random.uniform(2.0, 8.0))))
    repayment_frequency = factory.Iterator(['Monthly', 'Fortnightly', 'Weekly'])
    product_id = factory.Sequence(lambda n: f'PROD-{n:03d}')
    estimated_settlement_date = factory.Faker('future_date', end_date='+90d')
    broker = factory.SubFactory(BrokerFactory)
    branch = factory.LazyAttribute(lambda obj: obj.broker.branch if obj.broker else None)
    security_address = factory.Faker('street_address')
    security_type = factory.Iterator(['Residential', 'Commercial', 'Land', 'Industrial'])
    security_value = factory.LazyFunction(lambda: Decimal(str(random.randint(100000, 1000000))))
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)
    
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
    
    @factory.post_generation
    def bd(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.bd = extracted
        else:
            # Create a default BDM if none provided and if branch exists
            if self.branch:
                bdm = BDMFactory(branch=self.branch)
                self.bd = bdm


class DraftApplicationFactory(ApplicationFactory):
    """
    Factory for draft applications.
    """
    
    stage = 'draft'


class SubmittedApplicationFactory(ApplicationFactory):
    """
    Factory for submitted applications.
    """
    
    stage = 'app_submitted'
    created_at = factory.Faker('date_time_this_month')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(days=random.randint(1, 3)))


class ApprovedApplicationFactory(ApplicationFactory):
    """
    Factory for approved applications.
    """
    
    stage = 'formal_approval'
    created_at = factory.Faker('date_time_this_month')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(days=random.randint(3, 10)))
    
    @factory.post_generation
    def signature(self, create, extracted, **kwargs):
        if create:
            # Store the username as a string since signed_by is a CharField, not a ForeignKey
            self.signed_by = self.created_by.username
            self.signature_date = self.updated_at
            self.save()


class RejectedApplicationFactory(ApplicationFactory):
    """
    Factory for rejected applications.
    """
    
    stage = 'declined'
    created_at = factory.Faker('date_time_this_month')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(days=random.randint(3, 10)))


class FundedApplicationFactory(ApplicationFactory):
    """
    Factory for funded applications.
    """
    
    stage = 'settled'
    created_at = factory.Faker('date_time_this_month')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(days=random.randint(10, 20)))
    
    @factory.post_generation
    def signature(self, create, extracted, **kwargs):
        if create:
            # Store the username as a string since signed_by is a CharField, not a ForeignKey
            self.signed_by = self.created_by.username
            self.signature_date = self.created_at + timedelta(days=random.randint(3, 7))
            self.save()


class ClosedApplicationFactory(ApplicationFactory):
    """
    Factory for closed applications.
    """
    
    stage = 'closed'
    created_at = factory.Faker('date_time_between', start_date='-6m', end_date='-1m')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(days=random.randint(30, 60)))
    
    @factory.post_generation
    def signature(self, create, extracted, **kwargs):
        if create:
            # Store the username as a string since signed_by is a CharField, not a ForeignKey
            self.signed_by = self.created_by.username
            self.signature_date = self.created_at + timedelta(days=random.randint(3, 7))
            self.save()


class PurchaseApplicationFactory(ApplicationFactory):
    """
    Factory for purchase applications.
    """
    
    purpose = 'Purchase'
    
    @factory.post_generation
    def purchase_details(self, create, extracted, **kwargs):
        if create:
            # Add any purchase-specific details here if the model supports them
            pass


class RefinanceApplicationFactory(ApplicationFactory):
    """
    Factory for refinance applications.
    """
    
    purpose = 'Refinance'
    
    @factory.post_generation
    def refinance_details(self, create, extracted, **kwargs):
        if create:
            # Add any refinance-specific details here if the model supports them
            pass


class ConstructionApplicationFactory(ApplicationFactory):
    """
    Factory for construction applications.
    """
    
    purpose = 'Construction'
    
    @factory.post_generation
    def construction_details(self, create, extracted, **kwargs):
        if create:
            # Add construction-specific details using faker directly
            faker = factory.Faker._get_faker()
            self.qs_company_name = faker.company()
            self.qs_contact_name = faker.name()
            self.qs_phone = faker.phone_number()
            self.qs_email = faker.email()
            self.qs_report_date = faker.date_this_month()
            self.save()


class InvestmentApplicationFactory(ApplicationFactory):
    """
    Factory for investment applications.
    """
    
    purpose = 'Investment'
    security_type = factory.Iterator(['Commercial', 'Multi-Family', 'Mixed Use'])
    
    @factory.post_generation
    def investment_details(self, create, extracted, **kwargs):
        if create:
            # Add any investment-specific details here if the model supports them
            pass
