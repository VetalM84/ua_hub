"""Models for HUB app."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# from apps.accounts.models import User


class Marker(models.Model):
    """Marker model. Shows a marker on a map."""

    latitude = models.FloatField(blank=False, verbose_name=_("Широта"))
    longitude = models.FloatField(blank=False, verbose_name=_("Долгота"))
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name=_("Категория")
    )
    comment = models.CharField(
        max_length=200, blank=True, verbose_name=_("Комментарий")
    )
    created_at = models.DateTimeField(default=now, verbose_name=_("Дата"))
    # owner = models.ForeignKey(
    #     "User", on_delete=models.PROTECT, verbose_name=_("Владелец")
    # )
    ip = models.CharField(max_length=128, blank=False, verbose_name=_("IP адрес"))

    def __str__(self):
        return _(f"Маркер №{self.pk} от {self.created_at}. {self.category}")

    class Meta:
        verbose_name = _("Маркер")
        verbose_name_plural = _("Маркеры")
        ordering = ["created_at"]


class Category(models.Model):
    RATING_VALUES = (
        ("blue", _("Синий")),
        ("red", _("Красный")),
        ("green", _("Зеленый")),
        ("yellow", _("Желтый")),
        ("orange", _("Оранжевый")),
    )
    name = models.CharField(max_length=50, verbose_name=_("Название"))
    icon = models.ForeignKey("Icon", on_delete=models.PROTECT, verbose_name=_("Иконка"))
    color = models.CharField(max_length=1, verbose_name=_("Цвет"))

    def __str__(self):
        return _(f"{self.name}, {self.icon.name}, {self.color}")

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]


class Icon(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Название"))

    def __str__(self):
        return _({self.name})

    class Meta:
        verbose_name = _("Иконка")
        verbose_name_plural = _("Иконки")
        ordering = ["name"]
