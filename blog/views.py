from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404, Http404

from pages.models import Pages
from .models import Post


def post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
    except Pages.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, "blog/post.html", {"post": post})


class Posts(ListView):
    model = Post
    paginate_by = 1
    context_object_name = "posts"
    template_name = "blog/index.html"
    ordering = "-published_date"

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "blog/posts.html"
        else:
            return self.template_name
