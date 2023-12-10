from django.urls import path
from .apps import OnlineQueueConfig
from .views import queue_list, index, queue_admin

app_name = OnlineQueueConfig.name

urlpatterns = (
    path("", index, name="enqueue_form"),
    path("queue-list/", queue_list, name="queue_list"),
    path("queue-list-administration/", queue_admin, name="queue_management"),
)
