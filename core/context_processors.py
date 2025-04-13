from django.urls import resolve
from django.conf import settings

import core


def page_context(request):
    from .models import Page

    lookups = {}
    context = {}
    match = resolve(request.path)
    view = match.url_name
    if (app := match.namespace) is not None:
        if app in settings.EXCLUDE_FROM_PAGE:
            return {}
        lookups["app"] = app
    lookups["view"] = view
    if params := match.kwargs:
        lookups["params"] = list(params.values())

    try:
        page = Page.objects.get(**lookups)
    except core.models.Page.DoesNotExist:
        return {}
    context = {"title": page.title, "subtitle": page.subtitle, "blurb": page.blurb}
    return context
