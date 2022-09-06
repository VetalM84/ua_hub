"""Backend admin page."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User creation and changing forms on backend."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    # list of columns of users list on backend
    list_display = (
        "email",
        "get_full_name",
        "hometown",
        "date_joined",
        "is_staff",
    )
    list_filter = ("is_staff",)
    readonly_fields = (
        "get_full_name",
        "date_joined",
    )
    fieldsets = (
        # fields we see in Change User on backend
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "facebook_link",
                    "contacts",
                    "hometown",
                    "avatar",
                ),
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        # fields we see in Add User on backend
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    ordering = ("email",)
    search_fields = ("email",)
    filter_horizontal = ()


admin.site.unregister(Group)
