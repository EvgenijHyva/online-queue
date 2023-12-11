from .models import QueueCar
from django import forms
from django.utils.translation import gettext_lazy as _
from utils.constants import ServiceStatus, ServiceEnum
import json


class QueueForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate", "service", "status")
        help_texts = {
            "service": _("Please select the service."),
        }
        widgets = {
            "service": forms.Select(
                attrs={"class": "form-select"}, choices=ServiceStatus.choices
            ),
        }

    status = forms.CharField(
        initial=ServiceStatus.ADDED,
        widget=forms.HiddenInput(attrs={"readonly": "readonly"}),
    )
    plate = forms.CharField(
        help_text=_("Enter the license plate number of the car."),
        label=_("plate"),
        widget=forms.TextInput(attrs={"placeholder": _("License plate")}),
        min_length=3,
        max_length=15,
        strip=True,
        localize=True,
    )

    def serialize_instance_to_json(self):
        if self.instance:
            included_fields = [
                "plate",
                "created_at",
                "service",
                "status",
            ]

            instance_data = {
                field_name: getattr(self.instance, field_name)
                for field_name in included_fields
            }
            instance_data["created_at"] = instance_data["created_at"].isoformat()
            return instance_data

        else:
            raise ValueError("Form is not bound to an instance.")

    def dump_json_instance_to_string(self):
        serialized_data = self.serialize_instance_to_json()
        return json.dumps(serialized_data)
