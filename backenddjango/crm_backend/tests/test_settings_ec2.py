"""
Tests for the EC2 deployment settings.
"""

import os
import unittest
from importlib import import_module
from django.test import TestCase, override_settings


class EC2SettingsTestCase(TestCase):
    """Test case for EC2 deployment settings."""

    def test_ec2_settings_imports(self):
        """Test that the EC2 settings file can be imported without errors."""
        try:
            from crm_backend import settings_ec2
            self.assertTrue(True)  # If we get here, the import succeeded
        except ImportError:
            self.fail("Failed to import settings_ec2")

    def test_ec2_settings_values(self):
        """Test that the EC2 settings have the expected values."""
        from crm_backend import settings_ec2

        # Check that DEBUG is False
        self.assertFalse(settings_ec2.DEBUG)

        # Check that ALLOWED_HOSTS includes '*'
        self.assertIn('*', settings_ec2.ALLOWED_HOSTS)

        # Check that HTTPS enforcement is disabled
        self.assertFalse(settings_ec2.SECURE_SSL_REDIRECT)
        self.assertFalse(settings_ec2.SESSION_COOKIE_SECURE)
        self.assertFalse(settings_ec2.CSRF_COOKIE_SECURE)
        self.assertEqual(settings_ec2.SECURE_HSTS_SECONDS, 0)
        self.assertFalse(settings_ec2.SECURE_HSTS_INCLUDE_SUBDOMAINS)
        self.assertFalse(settings_ec2.SECURE_HSTS_PRELOAD)

        # Check that CORS is configured to allow all origins
        self.assertTrue(settings_ec2.CORS_ALLOW_ALL_ORIGINS)
        self.assertTrue(settings_ec2.CORS_ALLOW_CREDENTIALS)
        
        # Check additional security settings are properly configured for development
        self.assertEqual(settings_ec2.X_FRAME_OPTIONS, 'SAMEORIGIN')
        self.assertFalse(settings_ec2.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertFalse(settings_ec2.SECURE_BROWSER_XSS_FILTER)


if __name__ == '__main__':
    unittest.main()