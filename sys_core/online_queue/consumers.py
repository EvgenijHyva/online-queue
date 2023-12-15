import json
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.constants import ChannelRooms, ServiceStatus
from utils.utils import get_queue_cached_data, get_redis_connection, user_is_admin
from channels.db import database_sync_to_async
from .models import QueueCar

r = get_redis_connection()


class QueueConsumer(AsyncWebsocketConsumer):
    ROOM = ChannelRooms.QUEUE.name

    async def connect(self):
        self.user = self.scope.get("user", None)
        await self.logging_message({"message": f"User: '{str(self.user)}' connected"})
        await self.channel_layer.group_add(self.ROOM, self.channel_name)
        await self.accept()
        data = await get_queue_cached_data()
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"Connected to {self.ROOM} room",
                    "queue": data,
                }
            )
        )

    async def disconnect(self, close_code):
        await self.logging_message(
            {
                "message": f"User: '{str(self.user)}' disconnected from room '{self.ROOM}' with code: ({close_code})"
            }
        )
        await self.channel_layer.group_discard(self.ROOM, self.channel_name)

    async def send_queue_update(self, event):
        data = await get_queue_cached_data()
        await self.send(
            text_data=json.dumps({"message": event["message"], "queue": data})
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            handler_type = data.get("type", None)

            message_handlers = {
                "modify_queue": self.modify_queue,
            }

            handler = message_handlers.get(handler_type, self.handle_unknown_type)
            await handler(data)
        except json.JSONDecodeError:
            await self.send_error_message("Invalid JSON format")

    async def modify_queue(self, event):
        if self.user and user_is_admin(self.user):
            item = event.get("item", None)
            action = event.get("action", None)
            if item:
                await self.updateItem(item, action)
            else:
                await self.send_error_message("Corresponding object not sended")
        else:
            await self.logging_message(
                {
                    "message": "unauthorized access",
                    "details": f"{str(self.scope)}",
                    "user_details": f"User: {str(self.user)}",
                    "event": event,
                }
            )

    @database_sync_to_async
    def updateItem(self, item, action):
        print(item)
        queue = (
            QueueCar.objects.filter(
                is_active=True,
                plate=item.get("plate", None),
                service=item.get("service", None),
            )
            .order_by("-created_at")
            .first()
        )

        if not queue:
            return
        if action == "done":
            queue.status = ServiceStatus.DONE
            queue.save()

        elif action == "cancel":
            queue.status = ServiceStatus.CANCELED
            queue.save()

    async def handle_unknown_type(self, _):
        await self.send_error_message("Unknown type")

    async def send_error_message(self, details):
        await self.send(json.dumps({"status": "error", "details": details}))

    async def logging_message(self, event):
        print(event)
        print("#######################################")
