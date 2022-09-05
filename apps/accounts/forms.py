"""Forms management."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class UserLoginForm(AuthenticationForm):
    """User login form on frontend."""

    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserRegisterForm(UserCreationForm):
    """User register form on frontend."""

    first_name = forms.CharField(
        required=False,
        label=_("Имя"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        required=False,
        label=_("Фамилия"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label=_("Подтвердите пароль"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        required = False
        fields = ("first_name", "last_name", "email", "password1", "password2")


class CustomUserCreationForm(UserCreationForm):
    """Custom User creation form on backend."""

    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    """Custom User changing form on backend."""

    class Meta:
        model = User
        fields = "__all__"
