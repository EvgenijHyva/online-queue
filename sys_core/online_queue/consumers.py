import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.constants import ChannelRooms

r = redis.StrictRedis(host="localhost", port=6379, db=0)


class QueueConsumer(AsyncWebsocketConsumer):
    ROOM = ChannelRooms.QUEUE.name

    async def connect(self):
        print("connecting")
        await self.channel_layer.group_add(self.ROOM, self.channel_name)

        await self.accept()

        await self.send(
            text_data=json.dumps(
                {"type": "Connection established", "message": "Connected"}
            )
        )

    async def disconnect(self, close_code):
        print(
            f"Disconnected with code: ({close_code}), from room: '{self.ROOM}', channel: {self.channel_name}"
        )
        await self.channel_layer.group_discard(self.ROOM, self.channel_name)

    async def receive(self, text_data):
        print("call receive")
        data = json.loads(text_data)
        plate = data.get("plate")
        print("plate", plate)
        if plate:
            await self.send(
                text_data=json.dumps(
                    {"message": f"Plate {plate} has been added to the queue."}
                )
            )

    async def send_queue_update(self, event):
        print("Event", event)
        await self.send(text_data=json.dumps({"message": event["message"]}))

    async def group_send(self, data):
        print("Group send triggers")
        print(self)
        print(data)
