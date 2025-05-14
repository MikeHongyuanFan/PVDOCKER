"""
Tests for the Nginx configuration.
"""

import os
import unittest
import re


class NginxConfigTestCase(unittest.TestCase):
    """Test case for Nginx configuration."""

    def setUp(self):
        """Set up the test case."""
        self.nginx_config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'nginx', 'conf.d', 'app-dev.conf'
        )
        
        # Read the Nginx configuration file
        with open(self.nginx_config_path, 'r') as f:
            self.nginx_config = f.read()

    def test_nginx_config_exists(self):
        """Test that the Nginx configuration file exists."""
        self.assertTrue(os.path.exists(self.nginx_config_path))

    def test_nginx_listens_on_port_80(self):
        """Test that Nginx listens on port 80."""
        self.assertIn('listen 80', self.nginx_config)

    def test_nginx_no_https_redirect(self):
        """Test that Nginx doesn't redirect HTTP to HTTPS."""
        # Check for absence of redirect directives
        self.assertNotIn('return 301 https://', self.nginx_config)
        self.assertNotIn('return 302 https://', self.nginx_config)
        
        # Check for presence of absolute_redirect off directive
        self.assertIn('absolute_redirect off', self.nginx_config)

    def test_nginx_proxy_settings(self):
        """Test that Nginx proxy settings are correct."""
        self.assertIn('proxy_pass http://web:8000', self.nginx_config)
        self.assertIn('proxy_set_header Host $host', self.nginx_config)
        self.assertIn('proxy_set_header X-Real-IP $remote_addr', self.nginx_config)
        self.assertIn('proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for', self.nginx_config)
        # Check that X-Forwarded-Proto is set to http
        self.assertIn('proxy_set_header X-Forwarded-Proto http', self.nginx_config)
        
    def test_nginx_no_ssl_config(self):
        """Test that Nginx doesn't have any SSL configuration."""
        self.assertNotIn('ssl_certificate', self.nginx_config)
        self.assertNotIn('ssl_certificate_key', self.nginx_config)
        self.assertNotIn('listen 443', self.nginx_config)
        self.assertNotIn('ssl', self.nginx_config)


if __name__ == '__main__':
    unittest.main()