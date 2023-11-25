from django.core.management.base import BaseCommand
from online_queue.models import QueueCar


class Command(BaseCommand):
    help = "Dispose all existing queue"

    def handle(self, *args, **options):
        QueueCar.objects.update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all Queue instances to inactive")
        )
