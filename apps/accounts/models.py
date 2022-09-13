"""DB objects for User model."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager


class User(AbstractUser):
    """Custom User model."""

    username = None
    email = models.EmailField(blank=False, unique=True, verbose_name=_("Email"))
    facebook_link = models.URLField(
        blank=True, verbose_name=_("Facebook profile link")
    )
    contacts = models.CharField(blank=True, max_length=250, verbose_name=_("Contacts"))
    hometown = models.CharField(
        blank=True, max_length=250, verbose_name=_("Hometown")
    )
    avatar = models.ImageField(
        upload_to="avatar/",
        verbose_name=_("Image"),
        default="avatar/default_avatar.jpg",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Model representation."""
        return self.email

    def get_full_name(self):
        """Concatenate fist and last names."""
        full_name = " ".join([self.first_name, self.last_name])
        return full_name.strip()

    get_full_name.short_description = _("Full name")

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
