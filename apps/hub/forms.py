"""Form management for HUB app."""

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
                "placeholder": _("Широта"),
            }
        ),
    )
    longitude = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "longitude",
                "placeholder": _("Долгота"),
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=_("Выберите категорию"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "max-length": 200,
                    "placeholder": _("Комментарий, не обязательно"),
                }
            ),
        }


class UpdateMarkerForm(forms.ModelForm):
    """Form for updating marker on a frontend."""

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category"]
        widgets = {
            "latitude": forms.TextInput(attrs={"class": "form-control"}),
            "longitude": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "max-length": 200,
                    "placeholder": _("Комментарий, не обязательно"),
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
