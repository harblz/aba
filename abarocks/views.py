from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden

from django_htmx.http import retarget, trigger_client_event

from pages.models import Pages
from blog.models import Post


def home(request):
    try:
        Posts = Post.objects.order_by("-published_date")[:2]
    except Post.DoesNotExist:
        raise Http404("No recent blog posts")
    return render(request, "home.html", { 'Posts': Posts })

def about(request):
    return render(request, "about.html")

def patreon(request):
    return render(request, "patreon.html")

def login(request):
    return render(request, "login.html")

