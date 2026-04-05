from django.conf import settings
from django.urls import resolve

import core


def page_context(request) -> dict:
    from .models import Page

    lookups = {}
    context = {}
    match = resolve(request.path)
    view = match.url_name
    if app := match.namespace:
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


def nav_links(request):
    from .models import NavLink

    roots = NavLink.objects.filter(root=True).order_by("root_pos")
    noroots = NavLink.objects.filter(root=False).order_by(
        "page__app", "page__view", "page__params"
    )
    nav = {}
    for root in roots:
        tab = {}
        view = root.page.url_string()
        tab["root"] = view
        """if root.has_children:
            tab["children"] = {}
            for link in noroots:
                if link.page.app == root.page.app:
                    child = {"view": link.page.url_string()}
                    if link.page.params:
                        params = []
                        for param in link.page.params:
                            params.append(param)
                        child["params"] = params
                    tab["children"][link.label] = child
                else:
                    continue"""
        nav[root.label] = tab
    context = {"nav": nav}
    return context
