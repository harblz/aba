from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task


@receiver(pre_save, sender=Task)
def task_slug(sender, instance, **kwargs):
    if instance.slug is None:
        instance.slug = f"{instance.license.code}-{instance.area}-{instance.task}"
    else:
        pass
