from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.core.paginator import Paginator

from pages.models import Pages
from blog.models import Post


def home(request):
    posts = Post.objects.order_by("-published_date")
    if posts:
        paginator = Paginator(posts, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "home.html", {"page_obj": page_obj})
    else:
        return render(request, "home.html", {})


def about(request):
    return render(request, "about.html")


def patreon(request):
    return render(request, "patreon.html")


def login(request):
    return render(request, "login.html")
