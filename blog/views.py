import stripe

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect



def blog_coffee_checkout(request):
    stripe.api_key = "sk_test_GXRtTKknI00RdnWG9bXPy1iu"

    if request.method == "POST":
        token    = request.POST.get("stripeToken")

    try:
        charge  = stripe.Charge.create(
            amount      = token.amount,
            currency    = "usd",
            source      = token,
            description = "A generous donation from a fan!"
        )

        # new_car.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        #new_car.save()
        return render(request, 'blog/thanks.html', {})
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want


def blog_what_is_aba(request):
    return render(request, 'blog/blog_what_is_aba.html', {})

def blog_coffee(request):
    return render(request, 'blog/blog_coffee.html', {})

def blog_behavior_basics(request):
    return render(request, 'blog/blog_behavior_basics.html', {})

def blog_research(request):
    return render(request, 'blog/blog_research.html', {})

def blog_resources(request):
    return render(request, 'blog/blog_resources.html', {})

def blog_about(request):
    return render(request, 'blog/blog_about.html', {})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.page_views += 1;
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
