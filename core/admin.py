from django.contrib import admin
import pprint
from django.contrib.sessions.models import Session
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Navigation and URL Details",
            {
                "fields": ["app", "view", "params"],
                "description": "The details to reverse a page URL for the nav.",
            },
        ),
        (None, {"fields": ["nav"], "description": "Add page to the navigation bar?"}),
        (
            "Hero Content",
            {
                "fields": ["title", "subtitle", "blurb"],
                "description": "The content for the page Hero.",
            },
        ),
        (
            None,
            {
                "fields": ["body"],
                "description": "Any extra page content not saved elsewhere.",
            },
        ),
    ]


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    readonly_fields = ["page"]


"""class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace("\n", "<br>\n")

    _session_data.allow_tags = True
    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
    exclude = ["session_data"]
    date_hierarchy = "expire_date""" ""
