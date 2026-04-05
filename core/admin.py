from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

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
                "description": "The content for the page's Hero.",
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


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(SupportTicket)
class SupportMessageAdmin(admin.ModelAdmin):
    pass
