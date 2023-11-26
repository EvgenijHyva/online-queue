from .models import QueueCar
from django import forms
from django.utils.translation import gettext_lazy as _


class QueueForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate", "position", "service")

    position = forms.CharField(widget=forms.HiddenInput(), required=False)
    plate = forms.CharField(
        help_text=_("license_plate_help_text"),
        widget=forms.TextInput(attrs={"placeholder": _("license_plate")}),
    )
