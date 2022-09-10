"""Forms management."""

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
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


class UserProfileForm(forms.ModelForm):
    """User profile form on frontend."""

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
    hometown = forms.CharField(
        required=False,
        label=_("Родной город"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    facebook_link = forms.URLField(
        required=False,
        label=_("Facebook"),
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )
    contacts = forms.CharField(
        required=False,
        label=_("Контакты"),
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
    avatar = forms.ImageField(
        required=False,
        label=_("Изображение"),
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        exclude = ("password",)
        fields = (
            "first_name",
            "last_name",
            "hometown",
            "email",
            "facebook_link",
            "contacts",
            "avatar",
        )


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
