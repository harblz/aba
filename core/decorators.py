import functools
from django.http import HttpResponseForbidden


def htmx_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.htmx:
            return HttpResponseForbidden("Internal use only")
        return view_func(request, *args, **kwargs)

    return wrapper
