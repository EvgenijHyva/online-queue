from rest_framework import serializers
from .models import QueueCar


class QueueCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueCar
        fields = ["created_at", "plate", "is_active", "status", "service"]

    created_at = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)

    def get_created_at(self, instance) -> str:
        return instance.created_at.isoformat()

    def get_is_active(self, instance) -> str:
        return instance.is_active
