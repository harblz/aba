from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from pages.models import Pages
from .models import Post
from core.decorators import htmx_required
from .models import Post


def post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
    except Pages.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, "blog/post.html", {"post": post})


class Posts(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"
    template_name = "blog/index.html"
    ordering = "-published_date"

    def get_queryset(self):
        return Post.objects.filter(is_pinned=False).order_by(self.ordering)


def posts(request):
    all_posts = Post.objects.all().order_by("is_pinned", "-published_date")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return TemplateResponse(request, "blog/posts.html", {"page_obj": page_obj})
