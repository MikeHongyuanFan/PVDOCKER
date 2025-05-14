"""
Factory for User model.
"""

import factory
from factory.django import DjangoModelFactory
from users.models import User


class UserFactory(DjangoModelFactory):
    """
    Base factory for User model.
    """
    
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    role = 'client'
    phone = factory.Faker('phone_number')


class AdminUserFactory(UserFactory):
    """
    Factory for admin users.
    """
    
    username = factory.Sequence(lambda n: f'admin{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    role = 'admin'
    is_staff = True
    is_superuser = True


class BrokerUserFactory(UserFactory):
    """
    Factory for broker users.
    """
    
    username = factory.Sequence(lambda n: f'broker{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    role = 'broker'
    is_staff = False
    is_superuser = False


class ClientUserFactory(UserFactory):
    """
    Factory for client users.
    """
    
    username = factory.Sequence(lambda n: f'client{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    role = 'client'
    is_staff = False
    is_superuser = False


class StaffUserFactory(UserFactory):
    """
    Factory for staff users.
    """
    
    username = factory.Sequence(lambda n: f'staff{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    role = 'staff'
    is_staff = True
    is_superuser = False


class InactiveUserFactory(UserFactory):
    """
    Factory for inactive users.
    """
    
    is_active = False
