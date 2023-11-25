from django.shortcuts import render
from django.http import JsonResponse
from .models import QueueCar
import redis

r = redis.StrictRedis(host="localhost", port=6379, db=0)


def index(request):  # в противном случае переходит на страницу login
    context = {"title": "index"}
    return render(request, "online_queue/index.html", context)


def enqueue_user(request):
    return JsonResponse({"r": "render"})
