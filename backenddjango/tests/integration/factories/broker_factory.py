"""
Factory for Broker model.
"""

import factory
import random
from datetime import datetime, timedelta
from factory.django import DjangoModelFactory
from brokers.models import Broker, Branch, BDM
from .user_factory import BrokerUserFactory, UserFactory, StaffUserFactory


class BranchFactory(DjangoModelFactory):
    """
    Base factory for Branch model.
    """
    
    class Meta:
        model = Branch
    
    name = factory.Faker('company')
    address = factory.Faker('street_address')
    phone = factory.Faker('phone_number')
    email = factory.LazyAttribute(lambda obj: f'branch-{obj.name.lower().replace(" ", "-")}@example.com')
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)


class BrokerFactory(DjangoModelFactory):
    """
    Base factory for Broker model.
    """
    
    class Meta:
        model = Broker
    
    name = factory.Faker('name')
    company = factory.Faker('company')
    email = factory.LazyAttribute(lambda obj: f'{obj.name.lower().replace(" ", ".")}@{obj.company.lower().replace(" ", "")}.com')
    phone = factory.Faker('phone_number')
    address = factory.Faker('street_address')
    branch = factory.SubFactory(BranchFactory)
    user = factory.SubFactory(BrokerUserFactory)
    commission_bank_name = factory.Faker('company')
    commission_account_name = factory.LazyAttribute(lambda obj: obj.name)
    commission_account_number = factory.Sequence(lambda n: f'{random.randint(100000, 999999):06d}')
    commission_bsb = factory.Sequence(lambda n: f'{random.randint(100000, 999999):06d}')
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)


class BDMFactory(DjangoModelFactory):
    """
    Base factory for BDM (Business Development Manager) model.
    """
    
    class Meta:
        model = BDM
    
    name = factory.Faker('name')
    email = factory.LazyAttribute(lambda obj: f'bdm.{obj.name.lower().replace(" ", ".")}@example.com')
    phone = factory.Faker('phone_number')
    branch = factory.SubFactory(BranchFactory)
    user = factory.SubFactory(StaffUserFactory)
    created_by = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)
    
    @factory.post_generation
    def brokers(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for broker in extracted:
                self.bdm_brokers.add(broker)
        else:
            # Add 1-3 brokers by default
            num_brokers = random.randint(1, 3)
            for _ in range(num_brokers):
                broker = BrokerFactory()
                self.bdm_brokers.add(broker)


class ResidentialBrokerFactory(BrokerFactory):
    """
    Factory for residential brokers.
    """
    
    @factory.post_generation
    def specialization(self, create, extracted, **kwargs):
        if create:
            self.name = f"{self.name} - Residential Specialist"
            self.save()


class CommercialBrokerFactory(BrokerFactory):
    """
    Factory for commercial brokers.
    """
    
    @factory.post_generation
    def specialization(self, create, extracted, **kwargs):
        if create:
            self.name = f"{self.name} - Commercial Specialist"
            self.save()


class NewBrokerFactory(BrokerFactory):
    """
    Factory for new brokers.
    """
    
    created_at = factory.Faker('date_time_this_month')
    updated_at = factory.LazyAttribute(lambda obj: obj.created_at)


class SeniorBrokerFactory(BrokerFactory):
    """
    Factory for senior brokers.
    """
    
    # Use a fixed date that's at least 3 years ago to ensure the test passes
    @factory.lazy_attribute
    def created_at(self):
        return datetime.now() - timedelta(days=1095)  # 3 years ago
    
    updated_at = factory.Faker('date_time_between', start_date='-1y', end_date='now')


class MultiBranchBrokerFactory(BrokerFactory):
    """
    Factory for brokers with multiple branches.
    """
    
    @factory.post_generation
    def additional_branches(self, create, extracted, **kwargs):
        if not create:
            return
            
        num_branches = extracted if extracted else random.randint(1, 3)
        for _ in range(num_branches):
            branch = BranchFactory()
            # Note: This assumes there's a many-to-many relationship between Broker and Branch
            # If not, this would need to be adjusted based on the actual model relationship
