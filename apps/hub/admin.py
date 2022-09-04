"""Backend admin page."""

from django.contrib import admin

from apps.hub.models import Category, Icon, Marker


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category model views on backend."""

    list_display = ("id", "name", "icon", "color")
    list_display_links = ("id", "name")
    ordering = ("name",)
    search_fields = ("name",)


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

    list_display = ("id", "latitude", "longitude", "category", "created_at")
    list_display_links = ("id", "category")
    list_filter = ("category",)
    ordering = ("created_at", "category")
    search_fields = ("text",)
