"""Models for HUB app."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class Marker(models.Model):
    """Marker model. Shows a marker on a map."""

    latitude = models.FloatField(blank=False, verbose_name=_("Широта"))
    longitude = models.FloatField(blank=False, verbose_name=_("Долгота"))
    category = models.ForeignKey(
        to="Category", on_delete=models.PROTECT, verbose_name=_("Категория")
    )
    comment = models.CharField(
        max_length=200, blank=True, verbose_name=_("Комментарий")
    )
    created_at = models.DateTimeField(default=now, verbose_name=_("Дата"))
    owner = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Владелец"),
    )
    ip = models.CharField(max_length=128, blank=False, verbose_name=_("IP адрес"))

    def __str__(self):
        """Model representation."""
        return _(f"Маркер №{self.pk} от {self.created_at}. {self.category}")

    class Meta:
        verbose_name = _("Маркер")
        verbose_name_plural = _("Маркеры")
        ordering = ["created_at"]


class Category(models.Model):
    """Category model for marker."""

    name = models.CharField(max_length=50, verbose_name=_("Название"))
    icon = models.ForeignKey(
        to="Icon", on_delete=models.PROTECT, verbose_name=_("Иконка")
    )
    color = models.ForeignKey(
        to="Color", default="blue", on_delete=models.SET_DEFAULT, verbose_name=_("Цвет")
    )

    def __str__(self):
        """Model representation."""
        return _(f"{self.name}, {self.icon.name}, {self.color.name}")

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]


class Icon(models.Model):
    """Icon type model for marker."""

    name = models.CharField(max_length=100, verbose_name=_("Название"))

    def __str__(self):
        """Model representation."""
        return _({self.name})

    class Meta:
        verbose_name = _("Иконка")
        verbose_name_plural = _("Иконки")
        ordering = ["name"]


class Color(models.Model):
    """Color model for the marker."""

    name = models.CharField(max_length=100, verbose_name=_("Название"))

    def __str__(self):
        """Model representation."""
        return _({self.name})

    class Meta:
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")
        ordering = ["name"]
