"""Django signals."""

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.hub.models import Marker


@receiver(signal=[post_save, post_delete], sender=Marker)
def clear_cache(sender, **kwargs):
    """Method for clearing a cache after Marker model changes."""
    cache.delete("markers_frontend")
