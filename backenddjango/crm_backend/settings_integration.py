"""
Integration test settings for CRM Loan Management System.
This file extends the base settings and configures the environment for integration tests.
"""

import os
from datetime import timedelta
from .settings import DATABASES, REST_FRAMEWORK, MIDDLEWARE, SIMPLE_JWT, BASE_DIR

# Use in-memory SQLite database for faster test execution
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm_integration_test',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'crm_integration_test',
        },
    }
}

# Disable debug for integration tests to mimic production environment
DEBUG = False

# Use in-memory channel layer for WebSocket tests
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Disable throttling for integration tests
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
}

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable CSRF for API testing
MIDDLEWARE = [m for m in MIDDLEWARE if 'CsrfViewMiddleware' not in m]

# Configure media root for test file uploads
from tempfile import mkdtemp
MEDIA_ROOT = mkdtemp()

# Configure email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable Celery tasks during testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Increase JWT token lifetime for testing
SIMPLE_JWT = {
    **SIMPLE_JWT,
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Configure logging for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Test-specific settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_OUTPUT_DIR = os.path.join(BASE_DIR, 'test-results')
