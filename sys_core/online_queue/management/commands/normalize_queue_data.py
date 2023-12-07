from django.core.management.base import BaseCommand
from online_queue.models import QueueCar
from django.utils import timezone
from utils.constants import ServiceStatus


class Command(BaseCommand):
    help = "Normalize data for existing records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", action="store_true", help="Update all records regardless of date"
        )

    def handle(self, *args, **options):
        qs_filters = {
            "is_active": False,
            "status__in": [ServiceStatus.STARTED, ServiceStatus.ADDED],
        }

        if not options["all"]:
            today = timezone.now().date()
            qs_filters["created_at__date"] = today

        QueueCar.objects.filter(**qs_filters).update(status=ServiceStatus.CANCELED)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully normalized queue records {f'for {today}' if not options['all'] else ''}"
            )
        )
