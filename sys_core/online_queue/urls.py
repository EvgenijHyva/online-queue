from django.urls import path
from .apps import OnlineQueueConfig
from .views import queue_list, index

app_name = OnlineQueueConfig.name

urlpatterns = (
    path("", index, name="enqueue_form"),
    path("queue-list/", queue_list, name="queue_list"),
)
