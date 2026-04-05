from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post


def home(request):
    posts = Post.objects.order_by("-published_date").exclude(pinned=True)
    pinned = Post.objects.filter(pinned=True).order_by("published_date")
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


def divzero(request):
    x = 2 / 0
    return HttpResponse(str(x))
