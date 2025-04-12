from django.contrib import admin
import pprint
from django.contrib.sessions.models import Session
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    exclude = ["slug"]


"""class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace("\n", "<br>\n")

    _session_data.allow_tags = True
    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
    exclude = ["session_data"]
    date_hierarchy = "expire_date""" ""
