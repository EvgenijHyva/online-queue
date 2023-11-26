from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceEnum(models.TextChoices):
    TIRE_CHANGE = "A", _("Tire_change")
    WHEELWORK = "V", _("Wheelwork")
