from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import QueueCar


@receiver(pre_save, sender=QueueCar)
def handle_model_save(sender, instance: QueueCar, **kwargs):
    print("##############################")

    if instance.id:
        old_instance = QueueCar.objects.get(pk=instance.pk)
        if instance.is_object_changed(old_instance):
            print("Instances are different")
            print("Changed", instance.changed_fields(old_instance))
        #    print(f"State has changed from {old_instance.state} to {instance.state}")
