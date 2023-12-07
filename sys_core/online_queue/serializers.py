from rest_framework import serializers
from .models import QueueCar


class QueueCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueCar
        fields = ["created_at", "plate", "is_active", "status", "service"]

    created_at = serializers.SerializerMethodField(read_only=True)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()
