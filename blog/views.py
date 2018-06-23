import stripe

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from pages.models import Pages

from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect



def blog_coffee_checkout(request):
    stripe.api_key = "sk_live_0fHEU5T1nHoILQpYZ7lyPwP7"

    if request.method == "POST":
        token    = request.POST.get("stripeToken")
        donation = request.POST.get("donation")

    try:
        charge  = stripe.Charge.create(
            amount      = donation,
            currency    = "usd",
            source      = token,
            description = "A generous donation from a fan!"
        )

        # new_car.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        #new_car.save()
        donation = int(donation) / 100.00
        return render(request, 'blog/thanks.html', { 'donation' : donation })
        # The payment was successfully processed & the user's card was charged - confirm with them how much

def blog_coffee(request):
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_coffee.html', {'pages': pages})

def blog_research(request):
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_research.html', {'pages': pages})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/post_list.html', { 'posts': posts, 'pages': pages })

def post_details_by_id(request, pk):
    pages = Pages.objects.order_by('order')
    post = get_object_or_404(Post, pk=pk)
    post.page_views += 1;
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post, 'pages': pages})

def post_details_by_slug(request, slug):
    pages = Pages.objects.order_by('order')
    post = Post.objects.filter(slug=slug)
    post = get_object_or_404(Post, pk=post[0].id)
    post.page_views += 1;
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post, 'pages': pages})

def post_new(request):
    pages = Pages.objects.order_by('order')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details_by_id', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'pages': pages})

def post_edit(request, pk):
    pages = Pages.objects.order_by('order')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details_by_id', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'pages': pages})
