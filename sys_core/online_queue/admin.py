from django.contrib import admin
from online_queue.models import QueueCar


@admin.register(QueueCar)
class AdminQueueCar(admin.ModelAdmin):
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at", "id")
    list_display = ("plate", "is_active", "position", "created_at")
    search_fields = ("plate", "position")
