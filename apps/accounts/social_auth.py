"""Functions to extend social authentication."""

import requests
from django.core.files.base import ContentFile

from apps.accounts.models import User


def save_profile(backend, user, response, *args, **kwargs):
    """Save extra information to User instance upon singing in."""
    if backend.name == "facebook":
        profile = User.objects.get(pk=user.pk)
        profile.facebook_link = response.get("link")
        fb_hometown = response.get("hometown")
        profile.hometown = fb_hometown["name"]
        profile.save()
    elif backend.name == "google-oauth2":
        profile = User.objects.get(pk=user.pk)
        # get image with higher resolution equal to 300 instead of 96
        google_img_url = response.get("picture").replace("s96-c", "s300-c")
        name_from_email = user.email.split("@")
        image_content = ContentFile(requests.get(google_img_url).content)
        profile.avatar.save(f"{name_from_email[0]}.jpg", image_content)
