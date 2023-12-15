from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OnlineQueueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "online_queue"
    verbose_name = _("Online queue")

    def ready(self) -> None:
        import online_queue.signals

        return super().ready()
