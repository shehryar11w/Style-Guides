"""
Custom managers for models.
"""
from django.db import models


class ActiveManager(models.Manager):
    """Manager that returns only active objects."""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseManager(models.Manager):
    """Base manager with common queryset methods."""
    
    def active(self):
        """Return only active objects."""
        return self.filter(is_active=True)
    
    def recent(self, limit=10):
        """Return most recent objects."""
        return self.order_by('-created_at')[:limit]

