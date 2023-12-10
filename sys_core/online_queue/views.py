from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.utils import generate_redis_key, get_redis_connection
from django.contrib.auth.decorators import user_passes_test
from utils.constants import (
    ServiceEnum,
    ChannelRooms,
    RedisKeys,
    SERVICE_DICT,
    SERVICE_TIMING,
)
from .forms import QueueForm
import redis
import json

r = get_redis_connection()


def index(request):
    if request.POST:
        try:
            mutable_data = request.POST.copy()

            redis_key = generate_redis_key(mutable_data)
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

                messages.success(
                    request,
                    _("{plate} in queue, service - {service}").format(
                        plate=form.cleaned_data["plate"].upper(),
                        service=_(SERVICE_DICT[form.cleaned_data["service"]]),
                    ),
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
    print(services_trans)
    services_list = list(SERVICE_DICT.keys())
    services_timing = list(SERVICE_TIMING.values())
    services = list(zip(services_trans, services_list, services_timing))
    context = {
        "title": _("Online queue"),
        "services": services,
    }
    return render(request, "online_queue/queue_list.html", context)


@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def queue_admin(request):
    services = list(map(lambda x: _(x[1]), ServiceEnum.choices))
    print(services)
    context = {"title": _("Queue management"), "services": services}
    return render(request, "online_queue/queue_management.html", context)
