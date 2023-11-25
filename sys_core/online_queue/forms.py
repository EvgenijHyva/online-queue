from .models import QueueCar
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = QueueCar
        fields = ("plate",)
