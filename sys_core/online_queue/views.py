from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.constants import ServiceEnum, ChannelRooms
from .forms import QueueForm
from .consumers import QueueConsumer
import redis
import json

r = redis.StrictRedis(host="localhost", port=6379, db=0)


def index(request):
    if request.POST:
        try:
            mutable_data = request.POST.copy()
            existing_position = r.hget("queue_data", mutable_data["plate"])
            if existing_position:
                existing_data = json.loads(existing_position.decode("utf-8"))
                position = existing_data.get("position")
                messages.info(request, _("You have already in queue"))

            else:
                position = r.incr("queue_counter")
                mutable_data["position"] = position
                form = QueueForm(mutable_data)
                form.is_valid()
                form_data_json = json.dumps(form.cleaned_data)
                r.hset("queue_data", mutable_data["plate"], form_data_json)
                form.save()
                print("saved", form_data_json)
                messages.success(
                    request,
                    _("{plate} in queue with position {position}").format(
                        plate=form.cleaned_data["plate"].upper(),
                        position=position,
                    ),
                )
                # Notify clients about the new plate using WebSocket
                group_name = "queue_list"
                async_to_sync(QueueConsumer.group_send)(
                    ChannelRooms.QUEUE.name,
                    {
                        "type": "receive",
                        "plate": mutable_data["plate"],
                    },
                )

            return HttpResponseRedirect(reverse("queue:queue_list"))

        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")
            messages.error(
                request,
                _("Failed to add plate %(plate)s to the queue. Please try again.")
                % {"plate": mutable_data["plate"]},
            )
    else:
        form = QueueForm()

    context = {"title": _("Online queue"), "plate_register_form": form}
    return render(request, "online_queue/index.html", context)


def queue_list(request):
    services = list(map(lambda x: _(x[1]), ServiceEnum.choices))

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        ChannelRooms.QUEUE.name,
        {
            "type": "send.queue_update",
            "message": "Queue updated!",  # You can customize this message
        },
    )

    context = {"title": _("Online queue"), "services": services}

    return render(request, "online_queue/queue_list.html", context)
