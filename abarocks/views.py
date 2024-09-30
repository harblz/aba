from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden

from django_htmx.http import retarget, trigger_client_event


def home(request):
    return HttpResponse("This is a test of the site. It worked!")
