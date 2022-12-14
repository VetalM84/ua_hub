"""Django signals."""

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import get_language

from apps.hub.models import Category, Comment, Marker


@receiver(signal=post_delete, sender=Marker, dispatch_uid="marker_deleted", weak=False)
def clear_cache_delete_handler(sender, **kwargs):
    """Method for clearing a cache on home page after Marker instance has been deleted."""
    cache.delete("markers_frontend")


@receiver(signal=post_save, sender=Marker, dispatch_uid="marker_updated", weak=False)
def clear_cache_save_handler(sender, **kwargs):
    """Method for clearing a cache on home page after Marker instance has been updated."""
    cache.delete("markers_frontend")


@receiver(
    signal=post_delete, sender=Category, dispatch_uid="category_deleted", weak=False
)
def clear_cache_delete_handler(sender, **kwargs):
    """Method for clearing a categories list cache on home page after Category instance has been deleted."""
    cache.delete("categories_names_frontend")


@receiver(
    signal=post_save, sender=Category, dispatch_uid="category_updated", weak=False
)
def clear_cache_save_handler(sender, **kwargs):
    """Method for clearing a categories list cache on home page after Category instance has been updated."""
    cache.delete("categories_names_frontend")


@receiver(
    signal=post_delete, sender=Comment, dispatch_uid="comment_deleted", weak=False
)
def clear_cache_delete_handler(sender, instance, **kwargs):
    """Method for clearing a cache on Marker page after Comment instance has been deleted."""
    marker_id = instance.marker_id
    key = f"marker_{marker_id}"
    cache.delete(key)


@receiver(signal=post_save, sender=Comment, dispatch_uid="comment_added", weak=False)
def clear_cache_save_handler(sender, instance, **kwargs):
    """Method for clearing a cache on Marker page after Comment instance has been added."""
    marker_id = instance.marker_id
    key = f"marker_{marker_id}"
    cache.delete(key)


@receiver(
    signal=post_delete, sender=Marker, dispatch_uid="user_deleted_marker", weak=False
)
def clear_cache_block(sender, instance, **kwargs):
    """Method for clearing a markers cache after Marker instance has been deleted."""
    user = instance.owner_id
    user_language = get_language()
    key = f"markers_user_{user}_{user_language}"
    cache.delete(key)


@receiver(
    signal=post_save, sender=Marker, dispatch_uid="user_updated_marker", weak=False
)
def clear_cache_block(sender, instance, **kwargs):
    """Method for clearing a markers cache after Marker instance has been updated."""
    user = instance.owner_id
    user_language = get_language()
    key = f"markers_user_{user}_{user_language}"
    cache.delete(key)


# @receiver(signal=post_save, sender=Marker, dispatch_uid="user_updated_marker")
# def clear_cache_block(sender, instance, **kwargs):
#     """Method for clearing a template block cache after Marker instance has been updated."""
#     user = instance.owner_id
#     user_language = get_language()
#     key = make_template_fragment_key("markers_list", [user, user_language])
#     cache.delete(key)
