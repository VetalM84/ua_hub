"""Models for HUB app."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class Marker(models.Model):
    """Marker model. Shows a marker on a map."""

    latitude = models.FloatField(blank=False, verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=False, verbose_name=_("Longitude"))
    category = models.ForeignKey(
        to="Category", on_delete=models.PROTECT, verbose_name=_("Category")
    )
    comment = models.CharField(max_length=200, blank=True, verbose_name=_("Comment"))
    created_at = models.DateTimeField(default=now, verbose_name=_("Date"))
    owner = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Owner"),
    )
    ip = models.GenericIPAddressField(
        max_length=128, null=True, verbose_name=_("IP address")
    )

    def __str__(self):
        """Model representation."""
        return f"Mark #{self.pk} ({self.category}) by {self.created_at.date().strftime('%d-%m-%Y')}."

    class Meta:
        verbose_name = _("Mark")
        verbose_name_plural = _("Marks")
        ordering = ["created_at"]


class Category(models.Model):
    """Category model for marker."""

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    icon = models.ForeignKey(
        to="Icon", on_delete=models.PROTECT, verbose_name=_("Icon")
    )
    color = models.ForeignKey(
        to="Color", on_delete=models.PROTECT, verbose_name=_("Color")
    )

    def __str__(self):
        """Model representation."""
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]


class Icon(models.Model):
    """Icon type model for marker."""

    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        """Model representation."""
        return self.name

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")
        ordering = ["name"]


class Color(models.Model):
    """Color model for the marker."""

    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        """Model representation."""
        return self.name

    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")
        ordering = ["name"]
