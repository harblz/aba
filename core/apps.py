from django.apps import AppConfig
from django.db.models.signals import post_save

class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        from . import signals
