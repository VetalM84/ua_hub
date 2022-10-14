"""Functions to extend social authentication."""

import requests
from django.core.files.base import ContentFile


def save_image_from_url(image_url, user):
    """Save image from url to file and then save to user model."""
    name_from_email = user.email.split("@")
    image_content = ContentFile(requests.get(image_url).content)
    return user.avatar.save(f"{name_from_email[0]}.jpg", image_content)


def save_profile(backend, user, response, *args, **kwargs):
    """Save extra information to User instance upon singing in."""
    if backend.name == "facebook":
        fb_img_url = (
            f"https://graph.facebook.com/{response['id']}"
            f"/picture?type=large&access_token={response['access_token']}"
        )
        save_image_from_url(fb_img_url, user)
        user.facebook_link = response.get("link")
        fb_hometown = response.get("hometown")
        user.hometown = fb_hometown["name"]

    elif backend.name == "google-oauth2":
        # get image with higher resolution equal to 300 instead of 96
        google_img_url = response.get("picture").replace("s96-c", "s300-c")
        save_image_from_url(google_img_url, user)

    elif backend.name == "github":
        save_image_from_url(response.get("avatar_url"), user)

    user.save()
