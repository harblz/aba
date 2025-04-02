from django.core.management.base import BaseCommand, CommandError
from django.urls import get_resolver


class LoadViews(BaseCommand):
    help = "Load all configured views as core.PageContent entries"

    def handle(self, *args, **options):
        pass
