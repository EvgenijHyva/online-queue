from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.constants import ServiceEnum, ServiceStatus


class QueueCar(models.Model):
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
