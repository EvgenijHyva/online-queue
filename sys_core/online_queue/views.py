from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import QueueCar
from .forms import QueueForm
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
                        plate=form.cleaned_data["plate"],
                        position=position,
                    ),
                )

            return HttpResponseRedirect(reverse("queue:enqueue_user"))

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


def enqueue_user(request):
    return JsonResponse({"r": "render"})
