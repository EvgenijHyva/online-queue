from django.core.management.base import BaseCommand
from online_queue.models import QueueCar
import redis

r = redis.StrictRedis(host="localhost", port=6379, db=0)


class Command(BaseCommand):
    help = "Dispose all existing queue"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Cache is flushed {r.keys()}"))
        r.flushall()
        QueueCar.objects.update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS("Successfully updated all Queue instances to inactive")
        )
