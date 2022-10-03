"""DB objects for User model."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail

from apps.accounts.managers import UserManager


class User(AbstractUser):
    """Custom User model."""

    username = None
    email = models.EmailField(blank=False, unique=True, verbose_name=_("Email"))
    facebook_link = models.URLField(blank=True, verbose_name=_("Facebook profile link"))
    contacts = models.CharField(blank=True, max_length=250, verbose_name=_("Contacts"))
    hometown = models.CharField(blank=True, max_length=250, verbose_name=_("Hometown"))
    start_coordinates = models.CharField(blank=True, max_length=100, verbose_name=_("Start coordinates"))
    avatar = ProcessedImageField(
        upload_to="avatar/",
        format="JPEG",
        options={"quality": 80},
        default="avatar/default_avatar.jpg",
        verbose_name=_("Image"),
    )
    avatar_xl = ImageSpecField(
        source="avatar",
        processors=[Thumbnail(150, 150)],
        format="JPEG",
    )
    avatar_l = ImageSpecField(
        source="avatar",
        processors=[Thumbnail(110, 110)],
        format="JPEG",
    )
    avatar_m = ImageSpecField(
        source="avatar",
        processors=[Thumbnail(50, 50)],
        format="JPEG",
    )
    avatar_s = ImageSpecField(
        source="avatar",
        processors=[Thumbnail(32, 32)],
        format="JPEG",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Model representation."""
        return self.email

    def get_absolute_url(self):
        """Get url to User's model instance."""
        return reverse_lazy("public-profile", kwargs={"user_id": self.pk})

    def get_full_name(self):
        """Concatenate fist and last names."""
        full_name = " ".join([self.first_name, self.last_name])
        return full_name.strip()

    get_full_name.short_description = _("Full name")

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
