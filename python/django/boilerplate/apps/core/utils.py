"""
Utility functions for the application.
"""
from django.core.exceptions import ValidationError


def validate_email_domain(email, allowed_domains):
    """
    Validate that email belongs to allowed domains.
    
    Args:
        email: Email address to validate
        allowed_domains: List of allowed domain names
    
    Returns:
        bool: True if email domain is allowed
    
    Raises:
        ValidationError: If email domain is not allowed
    """
    domain = email.split('@')[1] if '@' in email else None
    
    if not domain or domain not in allowed_domains:
        raise ValidationError(
            f'Email domain must be one of: {", ".join(allowed_domains)}'
        )
    
    return True

