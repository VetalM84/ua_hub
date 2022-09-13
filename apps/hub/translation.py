"""Register Models for translation."""

from django.utils.translation import gettext as _
from modeltranslation.translator import TranslationOptions, register

from .models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Translate Category model name."""

    fields = ("name",)
    fallback_values = _("-- sorry, no translation provided --")
