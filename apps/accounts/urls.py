"""URL path for user management on frontend."""

from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views import (
    ResetPasswordView,
    password_change,
    public_user_profile,
    user_login,
    user_logout,
    user_profile,
    user_register,
)

urlpatterns = [
    path("accounts/profile/", user_profile, name="profile"),
    path("profile-public/<int:user_id>/", public_user_profile, name="public-profile"),
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("password-change/", password_change, name="password_change"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
