"""Functions to extend social authentication."""

import requests
from django.core.files.base import ContentFile


def save_profile(backend, user, response, *args, **kwargs):
    """Save extra information to User instance upon singing in."""
    name_from_email = user.email.split("@")
    if backend.name == "facebook":
        fb_img_url = f"https://graph.facebook.com/{response['id']}" \
                     f"/picture?type=large&access_token={response['access_token']}"
        image_content = ContentFile(requests.get(fb_img_url).content)
        user.avatar.save(f"{name_from_email[0]}.jpg", image_content)
        user.facebook_link = response.get("link")
        fb_hometown = response.get("hometown")
        user.hometown = fb_hometown["name"]
        user.save()

    elif backend.name == "google-oauth2":
        # get image with higher resolution equal to 300 instead of 96
        google_img_url = response.get("picture").replace("s96-c", "s300-c")
        image_content = ContentFile(requests.get(google_img_url).content)
        user.avatar.save(f"{name_from_email[0]}.jpg", image_content)
        user.save()
