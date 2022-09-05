"""DB objects for User model."""

from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager


class User(AbstractUser):
    """Custom User model."""

    email = models.EmailField(blank=False, unique=True, verbose_name=_("email address"))
    username = models.CharField(max_length=150, unique=False, verbose_name=_("username"))
    dob = models.DateField(blank=True, null=True, verbose_name=_("Date of birth"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Model representation."""
        return self.email

    def get_full_name(self):
        """Concatenate fist and last names."""
        return " ".join([self.first_name, self.last_name])

    get_full_name.short_description = "Full name"

    def get_age(self):
        """Return age according to given dob."""
        if self.dob:
            today = date.today()
            return (
                today.year
                - self.dob.year
                - ((today.month, today.day) < (self.dob.month, self.dob.day))
            )
        return "None"

    get_age.short_description = "Age"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
