import json, redis
from online_queue.models import QueueCar
from online_queue.serializers import QueueCarSerializer
from channels.db import database_sync_to_async


@database_sync_to_async
def get_active_queue_from_DB():
    data = QueueCar.objects.filter(is_active=True)
    serializer = QueueCarSerializer(data, many=True)
    return serializer.data


async def get_queue_cached_data(r: redis.StrictRedis) -> dict[str, dict]:
    queue_data = r.hgetall("queue_data")

    print(queue_data)
    if not queue_data:
        qs_data = await get_active_queue_from_DB()
        if qs_data:
            for item in qs_data:
                redis_key = f'{item["plate"]}-{item["service"]}'
                r.hset("queue_data", redis_key, json.dumps(item))
            queue_data = r.hgetall("queue_data")

    queue_data = {
        key.decode("utf-8"): json.loads(value.decode("utf-8"))
        for key, value in queue_data.items()
    }

    return queue_data
