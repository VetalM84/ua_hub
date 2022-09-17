"""View methods for USER goes here."""

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from apps.accounts.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from apps.accounts.models import User


@login_required(redirect_field_name="login")
def user_profile(request):
    """User profile page."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated!"), extra_tags="success")
        else:
            messages.error(
                request, _("Please, correct the errors."), extra_tags="danger"
            )
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


def public_user_profile(request, user_id):
    """User public profile page."""
    user = get_object_or_404(
        User.objects.only(
            "id",
            "first_name",
            "last_name",
            "date_joined",
            "facebook_link",
            "contacts",
            "hometown",
            "avatar",
        ),
        pk=user_id,
    )
    return render(request, "accounts/profile-public.html", {"user": user})


@login_required(redirect_field_name="login")
def change_password(request):
    """User change password method."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, _("Password has been updated!"), extra_tags="success"
            )
            return redirect("change_password")
        else:
            messages.error(
                request, _("Please, correct the errors."), extra_tags="danger"
            )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})


def user_login(request):
    """User login method."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request, _("You have successfully signed in!"), extra_tags="success"
            )
            return redirect(to="markers")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """User logout method."""
    logout(request)
    return redirect(to="login")


def user_register(request):
    """User sign up method."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, _("You have successfully signed up!"), extra_tags="success"
            )
            return redirect(to="profile")
        else:
            messages.error(request, _("Error registering!"), extra_tags="danger")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
