from django.core.management.base import BaseCommand
from online_queue.models import QueueCar
from django.utils import timezone
from utils.constants import ServiceStatus
from utils.utils import get_redis_connection

r = get_redis_connection()


class Command(BaseCommand):
    help = "Dispose all existing queue from today"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", action="store_true", help="Update all records regardless of date"
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Cache is flushed {r.keys()}"))
        r.flushall()

        qs_filters = {"is_active": True}

        if not options["all"]:
            today = timezone.now().date()
            qs_filters["created_at__date"] = today

        QueueCar.objects.filter(**qs_filters).update(
            is_active=False, status=ServiceStatus.CANCELED
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all Queue instances to inactive")
        )
