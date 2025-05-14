"""
Factory for Repayment model.
"""

import factory
import random
from decimal import Decimal
from datetime import timedelta
from factory.django import DjangoModelFactory
from applications.models import Repayment
from .application_factory import FundedApplicationFactory


class RepaymentFactory(DjangoModelFactory):
    """
    Base factory for Repayment model.
    """
    
    class Meta:
        model = Repayment
    
    application = factory.SubFactory(FundedApplicationFactory)
    due_date = factory.Faker('date_time_this_year')
    amount = factory.LazyFunction(lambda: Decimal(str(random.randint(500, 5000))))
    status = 'pending'
    notes = factory.Faker('paragraph')
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)


class PendingRepaymentFactory(RepaymentFactory):
    """
    Factory for pending repayments.
    """
    
    status = 'pending'
    # Use date_time_this_month instead of date_this_month to avoid tzinfo issue
    due_date = factory.Faker('date_time_this_month')


class PaidRepaymentFactory(RepaymentFactory):
    """
    Factory for paid repayments.
    """
    
    status = 'paid'
    due_date = factory.Faker('date_time_this_month')
    paid_date = factory.LazyAttribute(lambda obj: obj.due_date - timedelta(days=random.randint(0, 5)))
    payment_amount = factory.LazyAttribute(lambda obj: obj.amount)
    invoice = factory.Sequence(lambda n: f'INV-{n:06d}')


class LateRepaymentFactory(RepaymentFactory):
    """
    Factory for late repayments.
    """
    
    status = 'late'
    due_date = factory.LazyAttribute(lambda obj: obj.created_at - timedelta(days=random.randint(1, 30)))
    
    @factory.post_generation
    def late_details(self, create, extracted, **kwargs):
        if create:
            self.notes = f"Payment is late. Due on {self.due_date.strftime('%Y-%m-%d')}."
            self.save()


class DefaultedRepaymentFactory(RepaymentFactory):
    """
    Factory for defaulted repayments.
    """
    
    status = 'defaulted'
    due_date = factory.LazyAttribute(lambda obj: obj.created_at - timedelta(days=random.randint(31, 90)))
    
    @factory.post_generation
    def default_details(self, create, extracted, **kwargs):
        if create:
            self.notes = f"Payment has defaulted. Due on {self.due_date.strftime('%Y-%m-%d')}. Collection process initiated."
            self.save()


class PartialRepaymentFactory(RepaymentFactory):
    """
    Factory for partial repayments.
    """
    
    status = 'partial'
    due_date = factory.Faker('date_time_this_month')
    paid_date = factory.LazyAttribute(lambda obj: obj.due_date)
    payment_amount = factory.LazyAttribute(lambda obj: obj.amount * Decimal(str(random.uniform(0.1, 0.9))))
    invoice = factory.Sequence(lambda n: f'INV-{n:06d}')
    
    @factory.post_generation
    def partial_details(self, create, extracted, **kwargs):
        if create:
            self.notes = f"Partial payment received. Remaining balance: {self.amount - self.payment_amount}"
            self.save()


class DeferredRepaymentFactory(RepaymentFactory):
    """
    Factory for deferred repayments.
    """
    
    status = 'deferred'
    due_date = factory.Faker('date_time_this_month')
    
    @factory.post_generation
    def deferral_details(self, create, extracted, **kwargs):
        if create:
            new_due_date = self.due_date + timedelta(days=random.randint(14, 60))
            self.notes = f"Payment deferred from {self.due_date.strftime('%Y-%m-%d')} to {new_due_date.strftime('%Y-%m-%d')}."
            self.save()
