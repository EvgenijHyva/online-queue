from .models import QueueCar
from django import forms
from django.utils.translation import gettext_lazy as _


class QueueForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate", "position", "service")
        help_texts = {
            "service": _("Your help text for the service field."),
        }
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
        }

    position = forms.CharField(widget=forms.HiddenInput(), required=False)
    plate = forms.CharField(
        help_text=_("Enter the license plate number of the car."),
        widget=forms.TextInput(attrs={"placeholder": _("License plate")}),
    )
