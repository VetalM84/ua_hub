"""Register Models for translation."""

from django.utils.translation import gettext as _
from modeltranslation.translator import TranslationOptions, translator

from .models import Category


class CategoryTranslationOptions(TranslationOptions):
    """Translate Category model name."""

    fields = ("name",)
    fallback_values = _("-- извините, нет перевода --")


translator.register(Category, CategoryTranslationOptions)
