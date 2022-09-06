"""Form management for HUB app."""

from django import forms

from .models import Marker


class AddMarkerForm(forms.ModelForm):
    """Form for adding a new marker on a frontend."""

    class Meta:
        model = Marker
        fields = ["latitude", "longitude", "comment", "category"]
        widgets = {
            "latitude": forms.TextInput(
                attrs={"class": "form-control", "id": "latitude"}
            ),
            "longitude": forms.TextInput(
                attrs={"class": "form-control", "id": "longitude"}
            ),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
