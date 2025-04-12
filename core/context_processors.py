from django.urls import resolve


def page_context(request):
    from .models import Page

    match = resolve(request.path)
    view = match.view_name
    app = match.app_name
    content = Page.objects.get(app=app, view=view)
    return {"content": content}
