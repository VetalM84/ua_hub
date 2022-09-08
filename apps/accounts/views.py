"""View methods for USER goes here."""

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from apps.accounts.forms import UserLoginForm, UserRegisterForm


@login_required(redirect_field_name="login")
def change_password(request):
    """User change password method."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
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
            messages.success(request, "You are logged in!")
            print("To change your password follow http://127.0.0.1:8000/password/")
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
            messages.success(request, "You have been registered!")
            print("To change your password follow http://127.0.0.1:8000/password/")
            # TODO add redirect
        else:
            messages.error(request, "Error registering!")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})
