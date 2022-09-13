"""Register Models for translation."""

from modeltranslation.translator import TranslationOptions, translator

from .models import Category


class CategoryTranslationOptions(TranslationOptions):
    """Translate Category model name."""

    fields = ("name",)


translator.register(Category, CategoryTranslationOptions)
