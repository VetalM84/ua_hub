"""View methods for USER goes here."""

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from apps.accounts.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from apps.accounts.models import User


@login_required(redirect_field_name="login")
def user_profile(request):
    """User profile page."""
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Профиль обновлен!"), "success")
        else:
            messages.error(request, _("Пожалуйста исправьте ошибки."), "danger")
    else:
        form = UserProfileForm(
            initial={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hometown": user.hometown,
                "facebook_link": user.facebook_link,
                "contacts": user.contacts,
            }
        )
    return render(request, "accounts/profile.html", {"form": form})


@login_required(redirect_field_name="login")
def change_password(request):
    """User change password method."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Пароль обновлен!"), "success")
            return redirect("change_password")
        else:
            messages.error(request, _("Пожалуйста исправьте ошибки."), "danger")
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
            messages.success(request, _("Вы успешно вошли!"), "success")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """User logout method."""
    logout(request)
    return redirect("login")


def user_register(request):
    """User sign up method."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Вы успешно зарегистрировались!"), "success")
            return redirect(to="profile")
        else:
            messages.error(request, _("Ошибка регистрации!"), "danger")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
