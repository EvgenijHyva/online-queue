from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum, auto


class ServiceEnum(models.TextChoices):
    TIRE_CHANGE = "A", _("Tire_change")
    WHEELWORK = "V", _("Wheelwork")


class ServiceStatus(models.TextChoices):
    ADDED = "A", _("Added")
    STARTED = "S", _("Started")
    CANCELED = "C", _("Canceled")
    DONE = "D", _("Done")


class ChannelRooms(Enum):
    QUEUE = auto()


class RedisKeys(Enum):
    queue_data = "queue_data"


SERVICE_DICT = dict((key, str(value)) for key, value in ServiceEnum.choices)
