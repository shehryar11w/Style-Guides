"""
Tests for core utilities.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.core.utils import validate_email_domain


class UtilsTest(TestCase):
    """Test cases for utility functions."""
    
    def test_validate_email_domain_valid(self):
        """Test email domain validation with valid domain."""
        allowed_domains = ['example.com', 'test.com']
        self.assertTrue(
            validate_email_domain('user@example.com', allowed_domains)
        )
    
    def test_validate_email_domain_invalid(self):
        """Test email domain validation with invalid domain."""
        allowed_domains = ['example.com', 'test.com']
        with self.assertRaises(ValidationError):
            validate_email_domain('user@invalid.com', allowed_domains)

