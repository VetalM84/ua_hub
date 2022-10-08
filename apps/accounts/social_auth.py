"""Functions to extend social authentication."""

from apps.accounts.models import User


def save_profile(backend, user, response, *args, **kwargs):
    """Save extra information to User instance upon singing in."""
    if backend.name == "facebook":
        profile = User.objects.get(pk=user.pk)
        profile.facebook_link = response.get("link")
        fb_hometown = response.get("hometown")
        profile.hometown = fb_hometown["name"]
        profile.save()
