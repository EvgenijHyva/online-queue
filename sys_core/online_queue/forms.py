from .models import QueueCar
from django import forms
from django.utils.translation import gettext_lazy as _
import json


class QueueForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate", "service")
        help_texts = {
            "service": _("Your help text for the service field."),
        }
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
        }

    plate = forms.CharField(
        help_text=_("Enter the license plate number of the car."),
        widget=forms.TextInput(attrs={"placeholder": _("License plate")}),
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
