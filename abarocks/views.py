from django.shortcuts import render
from django.utils import timezone

from pages.models import Pages
from blog.models import Post

def redirect_root(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/post_list.html', { 'posts': posts, 'pages': pages })

def redirect_research(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_research.html', { 'pages': pages })


def redirect_coffee(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_coffee.html', { 'pages': pages })