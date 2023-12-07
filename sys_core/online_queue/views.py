from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.constants import ServiceEnum, ChannelRooms, SERVICE_DICT, RedisKeys
from .serializers import QueueCarSerializer
from .forms import QueueForm
import redis
import json

r = redis.StrictRedis(host="localhost", port=6379, db=0)


def index(request):
    if request.POST:
        try:
            mutable_data = request.POST.copy()
            redis_key = f'{mutable_data["plate"]}-{mutable_data["service"]}'
            existing_position = r.hget(RedisKeys.queue_data.value, redis_key)

            if (
                existing_position
                and json.loads(existing_position.decode("utf-8"))["service"]
                == mutable_data["service"]
            ):
                messages.info(request, _("You have already in queue"))

            else:
                form = QueueForm(mutable_data)
                form.is_valid()
                form.save()
                form_data_json = form.dump_json_instance_to_string()
                r.hset(RedisKeys.queue_data.value, redis_key, form_data_json)

                print("saved", form_data_json)
                messages.success(
                    request,
                    _("{plate} in queue, service - {service}").format(
                        plate=form.cleaned_data["plate"].upper(),
                        service=_(SERVICE_DICT[form.cleaned_data["service"]]),
                    ),
                )
                # Notify clients about the new plate using WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    ChannelRooms.QUEUE.name,
                    {
                        "type": "send_queue_update",
                        "plate": mutable_data["plate"],
                        "message": "added to queue",
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
    services_trans = list(map(lambda x: _(x[1]), ServiceEnum.choices))
    services_list = list(SERVICE_DICT.keys())
    services = list(zip(services_trans, services_list))
    context = {
        "title": _("Online queue"),
        "services": services,
    }
    return render(request, "online_queue/queue_list.html", context)
