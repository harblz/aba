from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from blog.models import Post


def home(request):
    posts = Post.objects.order_by("-published_date").exclude(is_pinned=True)
    pinned = Post.objects.filter(is_pinned=True).order_by("published_date")
    if pinned:
        pass
    else:
        pinned = False
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"page_obj": page_obj, "pinned": pinned})


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def testdebug(request):
    x = 2 / 0
    return HttpResponse(str(x))
