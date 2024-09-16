#import stripe

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from pages.models import Pages

from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect


import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

def blog_coffee_checkout(request):
    pages = Pages.objects.order_by('order')
    stripe.api_key = "sk_live_ERSCcIQW6Na7l8VfnXUpD2RH00E1Q70EFF"

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
        return render(request, 'blog/thanks.html', { 'pages': pages, 'donation' : donation })
        # The payment was successfully processed & the user's card was charged - confirm with them how much

def thanks(request):
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/thanks.html', { 'pages': pages })



def blog_coffee(request):
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_coffee.html', {'pages': pages})

def blog_research(request):
    pages = Pages.objects.order_by('order')
    return render(request, 'blog/blog_research.html', {'pages': pages})

def get_post_by_id(request, pk):

    current_post    = Post.objects.get(pk=pk)

    prev_post       = Post.objects.filter(published_date__date__lt=current_post.published_date).order_by('-published_date')[0:1]
    
    data = serializers.serialize("json", prev_post)


    author = Post.objects.get(pk=pk).author
    author = author.first_name
    return JsonResponse({
            'post'      :  data,
            'author'    :  author,
            'id'        :  prev_post[0].id,
        })

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
