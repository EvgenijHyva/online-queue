from django.urls import path
from .apps import OnlineQueueConfig
from .views import enqueue_user, index

app_name = OnlineQueueConfig.name

urlpatterns = (
    path("", index, name="enqueue_form"),
    path("enqueue/", enqueue_user, name="enqueue_user"),
)
