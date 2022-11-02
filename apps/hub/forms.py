"""Form management for HUB app."""

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category, Marker


class AddMarkerForm(forms.ModelForm):
    """Form for adding a new marker on a frontend."""

    latitude = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "latitude",
                "placeholder": _("Latitude"),
            }
        ),
    )
    longitude = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "longitude",
                "placeholder": _("Longitude"),
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().only("name"),
        empty_label=_("Choose category"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    valid_till = forms.DateField(
        required=False,
        label=_("Valid till"),
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    image = forms.ImageField(
        required=False,
        label=_("Image"),
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category", "valid_till", "image"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "max-length": 2000,
                    "placeholder": _("Comment, not required"),
                }
            ),
        }


class UpdateMarkerForm(forms.ModelForm):
    """Form for updating marker on a frontend."""

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category", "valid_till"]
        widgets = {
            "latitude": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "max-length": 2000,
                    "placeholder": _("Comment, not required"),
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "valid_till": forms.SelectDateWidget(attrs={"class": "form-select"}),
        }


class ContactForm(forms.Form):
    """Contact for on frontend."""

    from_email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
            }
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
