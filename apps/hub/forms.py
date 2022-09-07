"""Form management for HUB app."""

from django import forms
from django.utils.translation import gettext as _

from .models import Category, Marker


class AddMarkerForm(forms.ModelForm):
    """Form for adding a new marker on a frontend."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=_("Выберите категорию"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category"]
        widgets = {
            "latitude": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "latitude",
                    "placeholder": _("Широта"),
                }
            ),
            "longitude": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "longitude",
                    "placeholder": _("Долгота"),
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": _("Комментарий, не обязательно"),
                }
            ),
        }
