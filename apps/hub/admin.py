"""Backend admin page."""

from django.contrib import admin
from imagekit.admin import AdminThumbnail
from modeltranslation.admin import TranslationAdmin

from apps.hub.models import Category, Comment, Icon, Marker


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category model views on backend."""

    list_display = ("id", "name", "icon", "color")
    list_display_links = ("id", "name")
    ordering = ("name",)
    search_fields = ("name",)


class TranslatedCategoryAdmin(CategoryAdmin, TranslationAdmin):
    """Translation for Category name on backend."""

    pass


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    """Icon model views on backend."""

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    """Marker model views on backend."""

    list_display = ("id", "owner", "category", "marker_thumbnail", "created_at")
    list_display_links = ("id", "category", "owner")
    list_filter = ("category",)
    ordering = ("created_at", "category")
    search_fields = ("text",)
    marker_thumbnail = AdminThumbnail(image_field="thumb_s")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment model views on backend."""

    list_display = ("id", "owner", "created_at")
    list_display_links = ("id", "owner")
    ordering = ("-created_at",)
    search_fields = ("comment_text",)


admin.site.unregister(Category)
admin.site.register(Category, TranslatedCategoryAdmin)
