from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
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
            print("is exists ->", existing_position)
            if existing_position:
                existing_data = json.loads(existing_position.decode("utf-8"))
                position = existing_data.get("position")

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
                    f"{form.cleaned_data['plate']} in queue with position {position}",
                )

            return HttpResponseRedirect(reverse("queue:enqueue_user"))

        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")
            messages.error(
                request,
                f"Failed to add plate {mutable_data['plate']} to the queue. Please try again.",
            )
    else:
        form = QueueForm()

    context = {"title": "Online queue", "plate_register_form": form}
    return render(request, "online_queue/index.html", context)


def enqueue_user(request):
    return JsonResponse({"r": "render"})
