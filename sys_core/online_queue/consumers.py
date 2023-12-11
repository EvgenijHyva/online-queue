import json
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.constants import ChannelRooms
from utils.utils import get_queue_cached_data, get_redis_connection, user_is_admin

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

        await self.modify_queue({"message": "test"})

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

    async def logging_message(self, event):
        print("#######################################")
        print("event", event)
        print("#######################################")

    async def modify_queue(self, event):
        print("modification")
        if self.user and user_is_admin(self.user):
            pass
        else:
            await self.logging_message(
                {
                    "message": "unauthorized access",
                    "details": f"{str(self.scope)}",
                    "user_details": f"User: {str(self.user)}",
                    "event": event,
                }
            )
