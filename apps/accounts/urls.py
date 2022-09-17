"""URL path for user management on frontend."""

from django.urls import path

from apps.accounts.views import (
    change_password,
    public_user_profile,
    user_login,
    user_logout,
    user_profile,
    user_register,
)

urlpatterns = [
    path("profile/", user_profile, name="profile"),
    path("profile-public/<int:user_id>/", public_user_profile, name="public-profile"),
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("password/", change_password, name="change_password"),
]
