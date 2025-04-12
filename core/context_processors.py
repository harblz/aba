from django.urls import resolve


def page_context(request):
    from .models import PageContent

    match = resolve(request.path)
    view = match.view_name
    content = PageContent.objects.get(view=view)
    return {"content": content}
