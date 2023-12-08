import json, redis
from online_queue.models import QueueCar
from online_queue.serializers import QueueCarSerializer
from channels.db import database_sync_to_async
from utils.constants import RedisKeys
from django.utils import timezone
from django.conf import settings
import redis


def get_redis_connection():
    HOST = settings.REDIS_HOST
    PORT = settings.REDIS_PORT
    return redis.StrictRedis(host=HOST, port=PORT, db=0)


def generate_redis_key(item: QueueCar) -> str:
    return f'{item["plate"]}-{item["service"]}-{item["status"]}'


@database_sync_to_async
def get_active_queue_from_DB():
    today = timezone.now().date()
    data = QueueCar.objects.filter(is_active=True, created_at__date=today)
    serializer = QueueCarSerializer(data, many=True)
    return serializer.data


async def get_queue_cached_data() -> dict[str, dict]:
    r = get_redis_connection()
    queue_data = r.hgetall(RedisKeys.queue_data.value)

    if not queue_data:
        qs_data = await get_active_queue_from_DB()
        if qs_data:
            for item in qs_data:
                redis_key = generate_redis_key(item)
                r.hset(RedisKeys.queue_data.value, redis_key, json.dumps(item))
            queue_data = r.hgetall(RedisKeys.queue_data.value)

    queue_data = {
        key.decode("utf-8"): json.loads(value.decode("utf-8"))
        for key, value in queue_data.items()
    }

    return queue_data
