from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import QueueCar
from utils.utils import get_redis_connection, generate_redis_key
from utils.constants import ChannelRooms, RedisKeys
import json


@receiver(pre_save, sender=QueueCar)
def handle_model_save(sender, instance: QueueCar, **kwargs):
    if instance.id:
        old_instance = QueueCar.objects.get(pk=instance.pk)
        if instance.is_object_changed(old_instance):
            r = get_redis_connection()
            changes = instance.changed_fields(old_instance)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                ChannelRooms.QUEUE.name,
                {
                    "type": "logging_message",
                    "message": f"Updates for {instance.plate}, presaving activity",
                    "updates": json.dumps(changes),
                },
            )
            print("message logged")

            redis_key_old = generate_redis_key(old_instance.to_dict())
            r.hdel(RedisKeys.queue_data.value, redis_key_old)


@receiver(pre_delete, sender=QueueCar)
def model_pre_delete_handler(sender, instance: QueueCar, **kwargs):
    r = get_redis_connection()
    redis_key = generate_redis_key(instance.to_dict())
    r.hdel(RedisKeys.queue_data.value, redis_key)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        ChannelRooms.QUEUE.name,
        {
            "type": "send_queue_update",
            "message": f"Deleted {instance.plate} from queue",
            "updates": instance.to_json(),
        },
    )
    print(instance)


@receiver(post_save, sender=QueueCar)
def handle_model_post_save(sender, instance: QueueCar, **kwargs):
    channel_layer = get_channel_layer()
    if instance.is_active:
        r = get_redis_connection()
        redis_key = generate_redis_key(instance.to_dict())
        r.hset(RedisKeys.queue_data.value, redis_key, instance.to_json())

        async_to_sync(channel_layer.group_send)(
            ChannelRooms.QUEUE.name,
            {
                "type": "send_queue_update",
                "plate": instance.plate,
                "message": "Queue Updated",
            },
        )
    else:
        async_to_sync(channel_layer.group_send)(
            ChannelRooms.QUEUE.name,
            {
                "type": "send_queue_update",
                "plate": instance.plate,
                "message": f"Item {instance.status}",
            },
        )
