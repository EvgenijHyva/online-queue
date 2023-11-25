from django.db import models
from django.utils.translation import gettext_lazy as _


class QueueCar(models.Model):
    class Meta:
        unique_together = ("position", "is_active")

    plate = models.CharField(_("plate"), max_length=15)
    position = models.SmallIntegerField(_("position"))
    is_active = models.BooleanField(_("is_active"), default=True, blank=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self):
        return f"{self.plate} - Position: {self.position}"
