from .models import QueueCar
from django import forms
from django.utils.translation import gettext_lazy as _


class QueueForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate", "position")

    position = forms.CharField(widget=forms.HiddenInput(), required=False)
    plate = forms.CharField(
        help_text="Enter the license plate number of the car.",
        widget=forms.TextInput(attrs={"placeholder": _("license_plate")}),
    )
