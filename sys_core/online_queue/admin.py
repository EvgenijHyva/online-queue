from django.contrib import admin
from online_queue.models import QueueCar


@admin.register(QueueCar)
class AdminQueueCar(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "is_active")
    ordering = ("-created_at", "id")
    list_display = ("plate", "is_active", "status", "service", "created_at")
    search_fields = ("plate", "service")
