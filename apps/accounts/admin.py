"""Backend admin page."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User creation and changing forms."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    # list of columns in admin users list
    list_display = (
        "email",
        "username",
        "get_full_name",
        "get_age",
        "created_at",
        "updated_at",
        "is_staff",
    )
    list_filter = ("is_staff",)
    readonly_fields = (
        "get_full_name",
        "get_age",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        # fields we see in Change User
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
                    "username",
                    "dob",
                    "first_name",
                    "last_name",
                ),
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        # fields we see in Add User
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
