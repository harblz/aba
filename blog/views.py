from django.conf import settings
from django.shortcuts import render, get_object_or_404, Http404
from django.utils import timezone

from pages.models import Pages
from .models import Post

def post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
    except Pages.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, "blog/post.html", {"post": post})

def posts(request):
    try:
        posts = Post.objects.order_by("-published_date").values()
    except Pages.DoesNotExist:
        raise Http404("There are no published posts")
    return render(request, "blog/posts.html", {"posts": posts})