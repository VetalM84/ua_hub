"""Models for HUB app."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import SmartResize, Thumbnail

from apps.accounts.models import User


class Marker(models.Model):
    """Marker model. Shows a marker on a map."""

    latitude = models.FloatField(blank=False, verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=False, verbose_name=_("Longitude"))
    category = models.ForeignKey(
        to="Category", on_delete=models.PROTECT, verbose_name=_("Category")
    )
    comment = models.TextField(max_length=2000, blank=True, verbose_name=_("Comment"))
    created_at = models.DateTimeField(default=now, verbose_name=_("Date"))
    owner = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="markers",
        verbose_name=_("Owner"),
    )
    like = models.ManyToManyField(
        to=User, related_name="likes", default=None, blank=True, verbose_name=_("Like")
    )
    likes_count = models.BigIntegerField(default="0", verbose_name=_("Likes count"))
    ip = models.GenericIPAddressField(
        max_length=128, null=True, verbose_name=_("IP address")
    )
    image = ProcessedImageField(
        upload_to="marker/",
        blank=True,
        format="JPEG",
        options={"quality": 90},
        verbose_name=_("Image"),
    )
    image_preview_bg = ImageSpecField(
        source="image",
        processors=[SmartResize(646, 140)],
        format="JPEG",
    )
    thumb_s = ImageSpecField(
        source="image",
        processors=[Thumbnail(32, 32)],
        format="JPEG",
    )

    def __str__(self):
        """Model representation."""
        return f"Mark #{self.pk} ({self.category}) by {self.created_at.date().strftime('%d-%m-%Y')}."

    class Meta:
        verbose_name = _("Mark")
        verbose_name_plural = _("Marks")
        ordering = ["created_at"]


class Comment(models.Model):
    """Comment model for Marker."""

    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name=_("Owner")
    )
    marker = models.ForeignKey(
        to="Marker",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("Mark"),
    )
    comment_text = models.TextField(
        blank=False, max_length=300, verbose_name=_("Comment")
    )
    created_at = models.DateTimeField(default=now, verbose_name=_("Date"))

    def __str__(self):
        return self.marker.pk

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class Category(models.Model):
    """Category model for marker."""

    COLORS = (
        ("cadetblue", "cadetblue"),
        ("green", "green"),
        ("blue", "blue"),
        ("red", "red"),
        ("purple", "purple"),
        ("lightgreen", "lightgreen"),
        ("darkblue", "darkblue"),
        ("orange", "orange"),
        ("gray", "gray"),
        ("pink", "pink"),
        ("lightblue", "lightblue"),
        ("lightgray", "lightgray"),
        ("darkgreen", "darkgreen"),
        ("darkred", "darkred"),
        ("black", "black"),
    )
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    icon = models.ForeignKey(
        to="Icon", on_delete=models.PROTECT, verbose_name=_("Icon")
    )
    color = models.CharField(choices=COLORS, max_length=50, verbose_name=_("Color"))

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
