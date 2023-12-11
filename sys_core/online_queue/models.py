from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.constants import ServiceEnum, ServiceStatus
from django.core.serializers.json import DjangoJSONEncoder
import json


class QueueCar(models.Model):
    class Meta:
        verbose_name = _("Queue")
        verbose_name_plural = _("Queue")

    plate = models.CharField(_("plate"), max_length=15)
    is_active = models.BooleanField(_("is_active"), default=True, blank=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    service = models.CharField(
        _("service"),
        max_length=1,
        choices=ServiceEnum.choices,
        default=ServiceEnum.TIRE_CHANGE,
    )
    status = models.CharField(
        _("status"),
        max_length=1,
        choices=ServiceStatus.choices,
        default=ServiceStatus.ADDED,
    )

    def __str__(self):
        return f"{self.plate} - created: {self.created_at}"

    def save(self, *args, **kwargs):
        if self.is_active and self.status in [
            ServiceStatus.DONE,
            ServiceStatus.CANCELED,
        ]:
            self.is_active = False
        elif not self.is_active and self.status in [
            ServiceStatus.STARTED,
            ServiceStatus.ADDED,
        ]:
            self.is_active = True
        super(QueueCar, self).save(*args, **kwargs)

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DjangoJSONEncoder)

    def to_dict(self) -> dict[str, str]:
        return {
            "plate": self.plate,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "service": self.service,
            "status": self.status,
        }

    def is_object_changed(self, other: "QueueCar") -> bool:
        return self.to_json() != other.to_json()

    def changed_fields(self, other: "QueueCar") -> dict[str, str]:
        old = other.to_dict()
        new = self.to_dict()
        return dict(
            (new_key, str(new_value))
            for new_key, new_value in new.items()
            if new_value != old[new_key]
        )
