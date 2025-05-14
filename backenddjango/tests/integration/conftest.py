"""
Configuration file for pytest integration tests.
This file contains fixtures and setup/teardown functions for integration tests.
Focused on admin user testing with 100% API access.
"""

import os
import pytest
import django
from django.conf import settings

# Set the Django settings module to the integration test settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings_integration')
django.setup()

from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Set up the database for integration tests.
    This fixture runs once per test session.
    """
    with django_db_blocker.unblock():
        # Load any initial data needed for all tests
        call_command('loaddata', 'tests/integration/fixtures/initial_data.json')


@pytest.fixture
def api_client():
    """
    Return an API client for making requests.
    """
    return APIClient()


@pytest.fixture
def admin_user(db):
    """
    Create and return an admin user with full access.
    """
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    return user


@pytest.fixture
def admin_client(admin_user, api_client):
    """
    Return an API client authenticated as an admin user.
    """
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture(autouse=True)
def clear_media_root():
    """
    Clear the media root directory after each test.
    """
    yield
    import shutil
    if os.path.exists(settings.MEDIA_ROOT):
        for item in os.listdir(settings.MEDIA_ROOT):
            path = os.path.join(settings.MEDIA_ROOT, item)
            if os.path.isfile(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
