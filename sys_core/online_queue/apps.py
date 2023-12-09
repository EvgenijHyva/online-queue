from django.apps import AppConfig


class OnlineQueueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "online_queue"

    def ready(self) -> None:
        import online_queue.signals

        return super().ready()
