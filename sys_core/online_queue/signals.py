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
            changes = instance.changed_fields(old_instance)
            r = get_redis_connection()

            redis_key_old = generate_redis_key(old_instance.to_dict())
            redis_key_new = generate_redis_key(instance.to_dict())
            instance_json = instance.to_json()
            if instance.is_active:
                r.hdel(RedisKeys.queue_data.value, redis_key_old)
                r.hset(RedisKeys.queue_data.value, redis_key_new, instance_json)
            else:
                r.hdel(RedisKeys.queue_data.value, redis_key_old)
                r.hdel(RedisKeys.queue_data.value, redis_key_new)

            # send message thrue socket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                ChannelRooms.QUEUE.name,
                {
                    "type": "send_queue_update",
                    "message": f"updates for {instance.plate}",
                    "updates": json.dumps(changes),
                },
            )


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
    print("instance", instance.__dict__)
    print("kwarks", kwargs)
