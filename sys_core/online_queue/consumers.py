import json
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.constants import ChannelRooms
from utils.utils import get_queue_cached_data, get_redis_connection

r = get_redis_connection()


class QueueConsumer(AsyncWebsocketConsumer):
    ROOM = ChannelRooms.QUEUE.name

    async def connect(self):
        print("connecting")
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
        print(
            f"Disconnected with code: ({close_code}), from room: '{self.ROOM}', channel: {self.channel_name}"
        )
        await self.channel_layer.group_discard(self.ROOM, self.channel_name)

    async def send_queue_update(self, event):
        data = await get_queue_cached_data()
        await self.send(
            text_data=json.dumps({"message": event["message"], "queue": data})
        )

    async def logging_message(self, event):
        print("#######################################")
        print("self", self.__dict__)
        print("event", event)
        print("#######################################")
