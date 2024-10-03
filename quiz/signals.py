from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Quiz


@receiver(pre_save, sender=Quiz)
def task_slug(sender, instance, **kwargs):
    if instance.slug is None:
        instance.slug = f"{instance.course.code}-{instance.number}"
    else:
        pass
